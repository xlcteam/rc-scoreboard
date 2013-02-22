# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table('dance_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dance', ['Team'])

        # Adding model 'Group'
        db.create_table('dance_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dance', ['Group'])

        # Adding M2M table for field teams on 'Group'
        db.create_table('dance_group_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['dance.group'], null=False)),
            ('team', models.ForeignKey(orm['dance.team'], null=False))
        ))
        db.create_unique('dance_group_teams', ['group_id', 'team_id'])

        # Adding model 'Competition'
        db.create_table('dance_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dance', ['Competition'])

        # Adding M2M table for field groups on 'Competition'
        db.create_table('dance_competition_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm['dance.competition'], null=False)),
            ('group', models.ForeignKey(orm['dance.group'], null=False))
        ))
        db.create_unique('dance_competition_groups', ['competition_id', 'group_id'])

        # Adding model 'Event'
        db.create_table('dance_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dance', ['Event'])

        # Adding M2M table for field competitions on 'Event'
        db.create_table('dance_event_competitions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['dance.event'], null=False)),
            ('competition', models.ForeignKey(orm['dance.competition'], null=False))
        ))
        db.create_unique('dance_event_competitions', ['event_id', 'competition_id'])

        # Adding model 'Performance'
        db.create_table('dance_performance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='homelanders', to=orm['dance.Team'])),
            ('playing', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('referee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('dance', ['Performance'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table('dance_team')

        # Deleting model 'Group'
        db.delete_table('dance_group')

        # Removing M2M table for field teams on 'Group'
        db.delete_table('dance_group_teams')

        # Deleting model 'Competition'
        db.delete_table('dance_competition')

        # Removing M2M table for field groups on 'Competition'
        db.delete_table('dance_competition_groups')

        # Deleting model 'Event'
        db.delete_table('dance_event')

        # Removing M2M table for field competitions on 'Event'
        db.delete_table('dance_event_competitions')

        # Deleting model 'Performance'
        db.delete_table('dance_performance')


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
        'dance.competition': {
            'Meta': {'object_name': 'Competition'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dance.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dance.event': {
            'Meta': {'object_name': 'Event'},
            'competitions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dance.Competition']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dance.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dance.Team']", 'symmetrical': 'False'})
        },
        'dance.performance': {
            'Meta': {'object_name': 'Performance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playing': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'referee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'homelanders'", 'to': "orm['dance.Team']"})
        },
        'dance.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['dance']