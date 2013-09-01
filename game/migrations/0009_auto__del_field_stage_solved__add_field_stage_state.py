# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Stage.solved'
        db.delete_column(u'game_stage', 'solved')

        # Adding field 'Stage.state'
        db.add_column(u'game_stage', 'state',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Stage.solved'
        db.add_column(u'game_stage', 'solved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Stage.state'
        db.delete_column(u'game_stage', 'state')


    models = {
        u'game.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Stage']"})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'started_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'game.problem': {
            'Meta': {'object_name': 'Problem'},
            'base_points': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'io_description': ('django.db.models.fields.TextField', [], {}),
            'multiplier': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'out_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sample_in': ('django.db.models.fields.TextField', [], {}),
            'sample_out': ('django.db.models.fields.TextField', [], {})
        },
        u'game.stage': {
            'Meta': {'object_name': 'Stage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'problems'", 'to': u"orm['game.Problem']"}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': u"orm['teams.Team']"}),
            'unlocked_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'086b49707dbf44d5b88c591cee747cc2'", 'max_length': '32'})
        }
    }

    complete_apps = ['game']