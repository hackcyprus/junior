# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Problem'
        db.create_table(u'game_problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('html_template', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('multiplier', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('base_points', self.gf('django.db.models.fields.IntegerField')(default=300)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'game', ['Problem'])

        # Adding model 'Stage'
        db.create_table(u'game_stage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unlocked_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('points_earned', self.gf('django.db.models.fields.FloatField')()),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Problem'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'game', ['Stage'])

        # Adding model 'Attempt'
        db.create_table(u'game_attempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Stage'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'game', ['Attempt'])


    def backwards(self, orm):
        # Deleting model 'Problem'
        db.delete_table(u'game_problem')

        # Deleting model 'Stage'
        db.delete_table(u'game_stage')

        # Deleting model 'Attempt'
        db.delete_table(u'game_attempt')


    models = {
        u'game.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Stage']"})
        },
        u'game.problem': {
            'Meta': {'object_name': 'Problem'},
            'base_points': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'html_template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.stage': {
            'Meta': {'object_name': 'Stage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.FloatField', [], {}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Problem']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.Team']"}),
            'unlocked_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'6e61d7a5cfc2462d8f1637f9464dd1b5'", 'max_length': '32'})
        }
    }

    complete_apps = ['game']