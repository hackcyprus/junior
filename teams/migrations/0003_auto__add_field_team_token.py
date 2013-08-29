# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Team.token'
        db.add_column(u'teams_team', 'token',
                      self.gf('django.db.models.fields.CharField')(default='9ea1e24d9fd1439db5473d2d37af4402', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Team.token'
        db.delete_column(u'teams_team', 'token')


    models = {
        u'teams.participant': {
            'Meta': {'object_name': 'Participant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.Team']"})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'ca44bfa9a6d641d68244d258f3a6f189'", 'max_length': '32'})
        }
    }

    complete_apps = ['teams']