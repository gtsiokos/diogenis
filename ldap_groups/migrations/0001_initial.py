# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LDAPGroup'
        db.create_table('ldap_groups_ldapgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('make_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('make_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('org_unit', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('ldap_groups', ['LDAPGroup'])

        # Adding M2M table for field groups on 'LDAPGroup'
        db.create_table('ldap_groups_ldapgroup_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ldapgroup', models.ForeignKey(orm['ldap_groups.ldapgroup'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('ldap_groups_ldapgroup_groups', ['ldapgroup_id', 'group_id'])


    def backwards(self, orm):
        
        # Deleting model 'LDAPGroup'
        db.delete_table('ldap_groups_ldapgroup')

        # Removing M2M table for field groups on 'LDAPGroup'
        db.delete_table('ldap_groups_ldapgroup_groups')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ldap_groups.ldapgroup': {
            'Meta': {'ordering': "['org_unit']", 'object_name': 'LDAPGroup'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ldap_org_units'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'make_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'org_unit': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['ldap_groups']
