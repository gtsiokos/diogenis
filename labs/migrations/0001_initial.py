# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Lesson'
        db.create_table('labs_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('labs', ['Lesson'])

        # Adding model 'Classroom'
        db.create_table('labs_classroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('labs', ['Classroom'])

        # Adding model 'Lab'
        db.create_table('labs_lab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_hour', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('end_hour', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal('labs', ['Lab'])

        # Adding model 'TeacherToLab'
        db.create_table('labs_teachertolab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labs.Lesson'])),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labs.Teacher'])),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labs.Lab'])),
            ('max_students', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('labs', ['TeacherToLab'])

        # Adding model 'StudentToLesson'
        db.create_table('labs_studenttolesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AuthStudent'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labs.Lesson'])),
        ))
        db.send_create_signal('labs', ['StudentToLesson'])

        # Adding model 'StudentSubscription'
        db.create_table('labs_studentsubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teacher_to_lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labs.TeacherToLab'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AuthStudent'])),
            ('in_transit', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('labs', ['StudentSubscription'])

        # Adding model 'Teacher'
        db.create_table('labs_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('labs', ['Teacher'])


    def backwards(self, orm):
        
        # Deleting model 'Lesson'
        db.delete_table('labs_lesson')

        # Deleting model 'Classroom'
        db.delete_table('labs_classroom')

        # Deleting model 'Lab'
        db.delete_table('labs_lab')

        # Deleting model 'TeacherToLab'
        db.delete_table('labs_teachertolab')

        # Deleting model 'StudentToLesson'
        db.delete_table('labs_studenttolesson')

        # Deleting model 'StudentSubscription'
        db.delete_table('labs_studentsubscription')

        # Deleting model 'Teacher'
        db.delete_table('labs_teacher')


    models = {
        'accounts.authstudent': {
            'Meta': {'ordering': "['am']", 'object_name': 'AuthStudent', '_ormbases': ['accounts.UserProfile']},
            'am': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'introduction_year': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'accounts.userprofile': {
            'Meta': {'ordering': "['user']", 'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_teacher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
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
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'labs.classroom': {
            'Meta': {'ordering': "['name']", 'object_name': 'Classroom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'labs.lab': {
            'Meta': {'ordering': "['name', 'day', 'start_hour']", 'object_name': 'Lab'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'end_hour': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_hour': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        'labs.lesson': {
            'Meta': {'ordering': "['name']", 'object_name': 'Lesson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'labs.studentsubscription': {
            'Meta': {'object_name': 'StudentSubscription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_transit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.AuthStudent']"}),
            'teacher_to_lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labs.TeacherToLab']"})
        },
        'labs.studenttolesson': {
            'Meta': {'object_name': 'StudentToLesson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labs.Lesson']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.AuthStudent']"})
        },
        'labs.teacher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Teacher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'labs.teachertolab': {
            'Meta': {'ordering': "['lesson']", 'object_name': 'TeacherToLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labs.Lab']"}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labs.Lesson']"}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labs.Teacher']"})
        }
    }

    complete_apps = ['labs']
