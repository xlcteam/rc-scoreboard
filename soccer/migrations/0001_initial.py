# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table('soccer_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('soccer', ['Team'])

        # Adding model 'Match'
        db.create_table('soccer_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teamA', self.gf('django.db.models.fields.related.ForeignKey')(related_name='homelanders', to=orm['soccer.Team'])),
            ('teamB', self.gf('django.db.models.fields.related.ForeignKey')(related_name='foreigners', to=orm['soccer.Team'])),
            ('scoreA', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('scoreB', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('playing', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('referee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('soccer', ['Match'])

        # Adding model 'TeamResult'
        db.create_table('soccer_teamresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['soccer.Team'])),
            ('wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('draws', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('loses', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_shot', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_diff', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('matches_played', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('soccer', ['TeamResult'])

        # Adding model 'Group'
        db.create_table('soccer_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('soccer', ['Group'])

        # Adding M2M table for field teams on 'Group'
        db.create_table('soccer_group_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['soccer.group'], null=False)),
            ('team', models.ForeignKey(orm['soccer.team'], null=False))
        ))
        db.create_unique('soccer_group_teams', ['group_id', 'team_id'])

        # Adding M2M table for field matches on 'Group'
        db.create_table('soccer_group_matches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['soccer.group'], null=False)),
            ('match', models.ForeignKey(orm['soccer.match'], null=False))
        ))
        db.create_unique('soccer_group_matches', ['group_id', 'match_id'])

        # Adding M2M table for field results on 'Group'
        db.create_table('soccer_group_results', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['soccer.group'], null=False)),
            ('teamresult', models.ForeignKey(orm['soccer.teamresult'], null=False))
        ))
        db.create_unique('soccer_group_results', ['group_id', 'teamresult_id'])

        # Adding model 'Competition'
        db.create_table('soccer_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('soccer', ['Competition'])

        # Adding M2M table for field groups on 'Competition'
        db.create_table('soccer_competition_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm['soccer.competition'], null=False)),
            ('group', models.ForeignKey(orm['soccer.group'], null=False))
        ))
        db.create_unique('soccer_competition_groups', ['competition_id', 'group_id'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table('soccer_team')

        # Deleting model 'Match'
        db.delete_table('soccer_match')

        # Deleting model 'TeamResult'
        db.delete_table('soccer_teamresult')

        # Deleting model 'Group'
        db.delete_table('soccer_group')

        # Removing M2M table for field teams on 'Group'
        db.delete_table('soccer_group_teams')

        # Removing M2M table for field matches on 'Group'
        db.delete_table('soccer_group_matches')

        # Removing M2M table for field results on 'Group'
        db.delete_table('soccer_group_results')

        # Deleting model 'Competition'
        db.delete_table('soccer_competition')

        # Removing M2M table for field groups on 'Competition'
        db.delete_table('soccer_competition_groups')


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
        'soccer.competition': {
            'Meta': {'object_name': 'Competition'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['soccer.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'soccer.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['soccer.Match']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'results': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['soccer.TeamResult']", 'symmetrical': 'False'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['soccer.Team']", 'symmetrical': 'False'})
        },
        'soccer.match': {
            'Meta': {'object_name': 'Match'},
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playing': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'referee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'scoreA': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scoreB': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teamA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'homelanders'", 'to': "orm['soccer.Team']"}),
            'teamB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'foreigners'", 'to': "orm['soccer.Team']"})
        },
        'soccer.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'soccer.teamresult': {
            'Meta': {'object_name': 'TeamResult'},
            'draws': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goal_diff': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goal_shot': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'matches_played': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['soccer.Team']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['soccer']