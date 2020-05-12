
import builtins
from datetime import datetime, timedelta
from functools import wraps
import io
import logging
import os
import traceback

import boto3
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models.fields.files import FileField
from django.db.models.signals import post_delete, post_save
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from sapl.utils import hash_sha512


def _get_registration_key(model):
    return '%s_%s' % (model._meta.app_label, model._meta.model_name)


class Command(BaseCommand):

    s3c = None
    s3r = None

    bucket_name = 'cmjatai_portal'
    days_validate = 60

    start_time = None
    exec_time = 1800

    count_registros = 0

    def handle(self, *args, **options):
        post_delete.disconnect(dispatch_uid='sapl_post_delete_signal')
        post_save.disconnect(dispatch_uid='sapl_post_save_signal')
        post_delete.disconnect(dispatch_uid='cmj_post_delete_signal')
        post_save.disconnect(dispatch_uid='cmj_post_save_signal')

        self.logger = logging.getLogger(__name__)

        # self.close_files()
        self.s3_connect()
        # self.__clear_bucket('cmjatai_teste')
        self.start_time = timezone.localtime()
        self.s3_sync()

        print(self.start_time)
        print(timezone.localtime())
        print(self.count_registros)

        #self.s3_sync(only_reset=False, model_name='NormaJuridica')
        #self.s3_sync(app_label='sapl.norma', model_name='NormaJuridica')

        #obj = n = NormaJuridica.objects.get(pk=8727)
        #self.restore_file_from_object(self.bucket_name, obj)

    def restore_file_from_object(self, bucket_name, obj):
        b = self.get_bucket(bucket_name)

        for fn in obj.FIELDFILE_NAME:

            ff = getattr(obj, fn)
            if not ff:
                continue

            directory = os.path.dirname(ff.path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            if hasattr(ff, 'original_path'):
                directory = os.path.dirname(ff.original_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

            try:
                b.download_file(
                    ff.name,
                    ff.path
                )
            except Exception as e:
                print(e)

            if hasattr(ff, 'original_path'):
                try:
                    b.download_file(
                        ff.original_name,
                        ff.original_path
                    )
                except Exception as e:
                    print(e)

    def __clear_bucket(self, bucket_name):
        b = self.get_bucket(bucket_name)

        for o in b.objects.all():
            print(o)
            o.delete()

    def has_bucket(self, bucket_name):
        bs = self.s3r.buckets.all()
        for b in bs:
            if b.name == bucket_name:
                return True
        return False

    def get_bucket(self, bucket_name):
        bs = self.s3r.buckets.all()
        for b in bs:
            if b.name == bucket_name:
                return b
        raise Exception('Bucket não existe!')

    def s3_connect(self):

        access_key = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        try:
            self.s3c = boto3.client(
                's3',
                endpoint_url='https://lss.locawebcorp.com.br',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name='sa-east-1')
            self.s3r = boto3.resource(
                's3',
                endpoint_url='https://lss.locawebcorp.com.br',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name='sa-east-1')
        except:
            print('Erro na conexão com a locaweb')

    def s3_sync(self, app_label=None, model_name=None, only_reset=False):

        print('--------- Locaweb ----------')
        reset = False

        count = 0
        for app in apps.get_app_configs():
            if app_label and app.name != app_label:
                print(app.name)
                continue

            if not app.name.startswith('cmj') and not app.name.startswith('sapl'):
                continue
            print(app)

            for m in app.get_models():
                model_exec = False

                if model_name and m._meta.object_name != model_name:
                    continue

                for f in m._meta.get_fields():
                    dua = f
                    print(dua)
                    if hasattr(dua, 'auto_now') and dua.auto_now:
                        #print(m, 'auto_now deve ser desativado.')
                        # continue  # auto_now deve ser desativado
                        print(m, 'desativando auto_now')
                        dua.auto_now = False

                    if not isinstance(f, FileField):
                        continue

                    # se possui FileField, o model então
                    # deve possuir FIELDFILE_NAME
                    assert hasattr(m, 'FIELDFILE_NAME'), '{} não possui FIELDFILE_NAME'.format(
                        m._meta.label)

                    # se possui FileField, o model então
                    # deve possuir metadata
                    assert hasattr(m, 'metadata'), '{} não possui metadata'.format(
                        m._meta.label)

                    # o campo field deve estar em FIELDFILE_NAME
                    assert f.name in m.FIELDFILE_NAME, '{} não está no FIELDFILE_NAME de {}'.format(
                        f.name,
                        m._meta.label)

                    model_exec = True

                if not model_exec:
                    continue
                print(m)
                for i in m.objects.all().order_by('-id'):

                    if not hasattr(i, 'metadata'):
                        #print(i, 'não tem metadata')
                        continue
                    else:
                        if only_reset:
                            if i.metadata and \
                                    'locaweb' in i.metadata:
                                i.metadata['locaweb'] = {}
                                i.save()
                                print(i)
                            continue

                    metadata = i.metadata if i.metadata else {}
                    for fn in i.FIELDFILE_NAME:

                        ff = getattr(i, fn)
                        if not ff:
                            continue

                        # if hasattr(ff, 'original_path'):
                        #    self.checar_consistencia(i, ff, fn)
                        # continue

                        if not metadata:
                            metadata = {}

                        if 'locaweb' not in metadata:
                            metadata['locaweb'] = {}

                        if fn not in metadata['locaweb']:
                            metadata['locaweb'][fn] = {
                                'path': None,
                                'original_path': None,
                                'validate': None,
                                'hash': None,
                                'original_hash': None

                            }

                        if reset:
                            metadata['locaweb'][fn] = {
                                'path': None,
                                'original_path': None,
                                'validate': None,
                                'hash': None,
                                'original_hash': None
                            }

                        count_update = 0
                        try:
                            count_update += self.send_file(
                                metadata, i, ff, fn, 'path', 'hash')

                            count_update += self.send_file(
                                metadata, i, ff, fn, 'original_path', 'original_hash')

                        except Exception as e:
                            print(e)
                            print(count)
                            return
                        else:
                            if count_update:
                                i.metadata = metadata
                                i.save()
                                count += 1
                            else:
                                self.count_registros += 1

                            if (count == 500 or
                                    timezone.localtime() -
                                    self.start_time >
                                    timedelta(seconds=self.exec_time)):
                                return

    def checar_consistencia(self, i, ff, fn):
        try:
            existe_path = os.path.exists(ff.path)
            existe_original_path = os.path.exists(ff.original_path)
            if not existe_path:
                print('ARQUIVO PATH NÃO ENCONTRADO:',
                      i.id, i, ff.name)
            if not existe_original_path:
                dir_name = os.path.dirname(ff.original_path)
                list_dir = os.listdir(dir_name)
                if len(list_dir) == 1:
                    file_name = os.path.basename(ff.path)
                    original_file_rename_old = '{}/{}'.format(
                        dir_name, list_dir[0])
                    original_file_rename_new = '{}/{}'.format(
                        dir_name, file_name)

                    os.rename(original_file_rename_old,
                              original_file_rename_new)
                else:
                    print('ARQUIVO ORIGINAL PATH NÃO ENCONTRADO:',
                          i.id, i, ff.name, len(ff.name))
        except Exception as e:
            print(i, e)

    def temp_file_from_object(self, bucket_name, obj, fn, attr_path):

        ff = getattr(obj, fn)
        if not ff:
            return None

        if not hasattr(ff, attr_path):
            return None

        b = self.get_bucket(bucket_name)

        t_p = '/tmp/br.leg.go.jatai.portalcmj.{}.{}.{}.{}.{}'.format(
            attr_path,
            obj._meta.app_label,
            obj._meta.model_name,
            obj.id,
            fn
        )

        try:
            r_p = b.download_file(
                ff.name,
                t_p
            )

            return t_p

        except Exception as e:
            print(e)
            return False

    def validate_file(self, metadata, i, fn, attr_path, attr_hash):
        if metadata['locaweb'][fn]['validate']:
            v = parse_datetime(metadata['locaweb'][fn]['validate'])

            # if timezone.localtime() - v > timedelta(seconds=30):
            if self.start_time - v < timedelta(days=self.days_validate):
                return True

            t_p = self.temp_file_from_object(
                self.bucket_name,
                i,
                fn, attr_path
            )
            if t_p is None:
                return True
            if not t_p:
                return False

            hash = hash_sha512(t_p)

            if hash == metadata['locaweb'][fn][attr_hash]:
                return True

        else:
            print('Documento Sem validação:', i.id, i)
        return False

    def send_file(self, metadata, i, ff, fn, attr_path, attr_hash):

        if not hasattr(ff, attr_path):
            return 0

        if os.path.exists(getattr(ff, attr_path)):

            if metadata['locaweb'][fn][attr_path]:
                # return 0
                t = os.path.getmtime(getattr(ff, attr_path))
                date_file = datetime.fromtimestamp(t, timezone.utc)

                if parse_datetime(metadata['locaweb'][fn][attr_path]) > date_file:
                    result = self.validate_file(
                        metadata, i, fn, attr_path, attr_hash)
                    if result:
                        return 0
            # return 0
            print('Enviando...', i, attr_path)

            """self.s3c.upload_file(
                getattr(ff, attr_path),
                self.bucket_name,
                ff.original_name if 'original' in attr_path else ff.name,
                ExtraArgs={
                    'ACL': 'private',
                    'Metadata': {
                        'pk': f'{i._meta.label_lower}.{i.id}'
                    }
                }
            )"""

            obj = self.s3r.Object(
                self.bucket_name,
                ff.original_name if 'original' in attr_path else ff.name,
            )
            with open(getattr(ff, attr_path), "rb") as f:
                obj.upload_fileobj(
                    f,
                    ExtraArgs={
                        'ACL': 'private',
                        'Metadata': {
                            'pk': f'{i._meta.label_lower}.{i.id}'
                        }
                    })

            metadata['locaweb'][fn][attr_path] = timezone.localtime()
            metadata['locaweb'][fn][attr_hash] = hash_sha512(
                getattr(ff, attr_path))
            metadata['locaweb'][fn]['validate'] = timezone.localtime()

            return 1
        return 0