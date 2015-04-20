# -*- coding: utf-8 -*-
import openerp.http as http
import base64
from openerp import _, modules
from openerp.service import db as db_ws
import logging
_logger = logging.getLogger(__name__)


class RestoreDB(http.Controller):

    @http.route(
        '/restore_db',
        type='json',
        auth='none',
        )
    def restore_db(self, admin_pass, db_name, file_path, backups_state):
        _logger.info("Restoring database %s from %s" % (db_name, file_path))
        error = False
        try:
            f = file(file_path, 'r')
            data_b64 = base64.encodestring(f.read())
            f.close()
        except Exception, e:
            error = (_(
                'Unable to read file %s\n\
                This is what we get: \n %s') % (
                file_path, e))
            return {'error': error}
        try:
            db_ws.exp_restore(db_name, data_b64)
        except Exception, e:
            error = (_(
                'Unable to restore bd %s, this is what we get: \n %s') % (
                db_name, e))
            return {'error': error}

        # # disable or enable backups
        # TODO unificar con la que esta en database
        registry = modules.registry.RegistryManager.get(db_name)
        with registry.cursor() as db_cr:
            registry['ir.config_parameter'].set_param(
                db_cr, 1, 'database.backups.enable', str(backups_state))