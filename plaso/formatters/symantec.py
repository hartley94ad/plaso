# -*- coding: utf-8 -*-
"""This file contains a formatter for Symantec logs."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


__author__ = 'David Nides (david.nides@gmail.com)'


class SymantecFormatter(interface.ConditionalEventFormatter):
  """Define the formatting for Symantec events."""

  DATA_TYPE = 'av:symantec:scanlog'

  EVENT_NAMES = {
      '1': 'GL_EVENT_IS_ALERT',
      '2': 'GL_EVENT_SCAN_STOP',
      '3': 'GL_EVENT_SCAN_START',
      '4': 'GL_EVENT_PATTERN_UPDATE',
      '5': 'GL_EVENT_INFECTION',
      '6': 'GL_EVENT_FILE_NOT_OPEN',
      '7': 'GL_EVENT_LOAD_PATTERN',
      '8': 'GL_STD_MESSAGE_INFO',
      '9': 'GL_STD_MESSAGE_ERROR',
      '10': 'GL_EVENT_CHECKSUM',
      '11': 'GL_EVENT_TRAP',
      '12': 'GL_EVENT_CONFIG_CHANGE',
      '13': 'GL_EVENT_SHUTDOWN',
      '14': 'GL_EVENT_STARTUP',
      '16': 'GL_EVENT_PATTERN_DOWNLOAD',
      '17': 'GL_EVENT_TOO_MANY_VIRUSES',
      '18': 'GL_EVENT_FWD_TO_QSERVER',
      '19': 'GL_EVENT_SCANDLVR',
      '20': 'GL_EVENT_BACKUP',
      '21': 'GL_EVENT_SCAN_ABORT',
      '22': 'GL_EVENT_RTS_LOAD_ERROR',
      '23': 'GL_EVENT_RTS_LOAD',
      '24': 'GL_EVENT_RTS_UNLOAD',
      '25': 'GL_EVENT_REMOVE_CLIENT',
      '26': 'GL_EVENT_SCAN_DELAYED',
      '27': 'GL_EVENT_SCAN_RESTART',
      '28': 'GL_EVENT_ADD_SAVROAMCLIENT_TOSERVER',
      '29': 'GL_EVENT_REMOVE_SAVROAMCLIENT_FROMSERVER',
      '30': 'GL_EVENT_LICENSE_WARNING',
      '31': 'GL_EVENT_LICENSE_ERROR',
      '32': 'GL_EVENT_LICENSE_GRACE',
      '33': 'GL_EVENT_UNAUTHORIZED_COMM',
      '34': 'GL_EVENT_LOG_FWD_THRD_ERR',
      '35': 'GL_EVENT_LICENSE_INSTALLED',
      '36': 'GL_EVENT_LICENSE_ALLOCATED',
      '37': 'GL_EVENT_LICENSE_OK',
      '38': 'GL_EVENT_LICENSE_DEALLOCATED',
      '39': 'GL_EVENT_BAD_DEFS_ROLLBACK',
      '40': 'GL_EVENT_BAD_DEFS_UNPROTECTED',
      '41': 'GL_EVENT_SAV_PROVIDER_PARSING_ERROR',
      '42': 'GL_EVENT_RTS_ERROR',
      '43': 'GL_EVENT_COMPLIANCE_FAIL',
      '44': 'GL_EVENT_COMPLIANCE_SUCCESS',
      '45': 'GL_EVENT_SECURITY_SYMPROTECT_POLICYVIOLATION',
      '46': 'GL_EVENT_ANOMALY_START',
      '47': 'GL_EVENT_DETECTION_ACTION_TAKEN',
      '48': 'GL_EVENT_REMEDIATION_ACTION_PENDING',
      '49': 'GL_EVENT_REMEDIATION_ACTION_FAILED',
      '50': 'GL_EVENT_REMEDIATION_ACTION_SUCCESSFUL',
      '51': 'GL_EVENT_ANOMALY_FINISH',
      '52': 'GL_EVENT_COMMS_LOGIN_FAILED',
      '53': 'GL_EVENT_COMMS_LOGIN_SUCCESS',
      '54': 'GL_EVENT_COMMS_UNAUTHORIZED_COMM',
      '55': 'GL_EVENT_CLIENT_INSTALL_AV',
      '56': 'GL_EVENT_CLIENT_INSTALL_FW',
      '57': 'GL_EVENT_CLIENT_UNINSTALL',
      '58': 'GL_EVENT_CLIENT_UNINSTALL_ROLLBACK',
      '59': 'GL_EVENT_COMMS_SERVER_GROUP_ROOT_CERT_ISSUE',
      '60': 'GL_EVENT_COMMS_SERVER_CERT_ISSUE',
      '61': 'GL_EVENT_COMMS_TRUSTED_ROOT_CHANGE',
      '62': 'GL_EVENT_COMMS_SERVER_CERT_STARTUP_FAILED',
      '63': 'GL_EVENT_CLIENT_CHECKIN',
      '64': 'GL_EVENT_CLIENT_NO_CHECKIN',
      '65': 'GL_EVENT_SCAN_SUSPENDED',
      '66': 'GL_EVENT_SCAN_RESUMED',
      '67': 'GL_EVENT_SCAN_DURATION_INSUFFICIENT',
      '68': 'GL_EVENT_CLIENT_MOVE',
      '69': 'GL_EVENT_SCAN_FAILED_ENHANCED',
      '70': 'GL_EVENT_MAX_event_name',
      '71': 'GL_EVENT_HEUR_THREAT_NOW_WHITELISTED',
      '72': 'GL_EVENT_INTERESTING_PROCESS_DETECTED_START',
      '73': 'GL_EVENT_LOAD_ERROR_COH',
      '74': 'GL_EVENT_LOAD_ERROR_SYKNAPPS',
      '75': 'GL_EVENT_INTERESTING_PROCESS_DETECTED_FINISH',
      '76': 'GL_EVENT_HPP_SCAN_NOT_SUPPORTED_FOR_OS',
      '77': 'GL_EVENT_HEUR_THREAT_NOW_KNOWN'
  }
  CATEGORY_NAMES = {
      '1': 'GL_CAT_INFECTION',
      '2': 'GL_CAT_SUMMARY',
      '3': 'GL_CAT_PATTERN',
      '4': 'GL_CAT_SECURITY'
  }
  ACTION_1_2_NAMES = {
      '1': 'Quarantine infected file',
      '2': 'Rename infected file',
      '3': 'Delete infected file',
      '4': 'Leave alone (log only)',
      '5': 'Clean virus from file',
      '6': 'Clean or delete macros'
  }
  ACTION_0_NAMES = {
      '1': 'Quarantined',
      '2': 'Renamed',
      '3': 'Deleted',
      '4': 'Left alone',
      '5': 'Cleaned',
      '6': ('Cleaned or macros deleted (no longer used as of '
            'Symantec AntiVirus 9.x)'),
      '7': 'Saved file as...',
      '8': 'Sent to Intel (AMS)',
      '9': 'Moved to backup location',
      '10': 'Renamed backup file',
      '11': 'Undo action in Quarantine View',
      '12': 'Write protected or lack of permissions - Unable to act on file',
      '13': 'Backed up file'
  }

  # The identifier for the formatter (a regular expression)
  FORMAT_STRING_SEPARATOR = u'; '
  FORMAT_STRING_PIECES = [
      u'Event Name: {event_map}',
      u'Category Name: {category_map}',
      u'Malware Name: {virus}',
      u'Malware Path: {file}',
      u'Action0: {action0_map}',
      u'Action1: {action1_map}',
      u'Action2: {action2_map}',
      u'Description: {description}',
      u'Scan ID: {scanid}',
      u'Event Data: {event_data}',
      u'Remote Machine: {remote_machine}',
      u'Remote IP: {remote_machine_ip}']

  FORMAT_STRING_SHORT_PIECES = [
      u'{file}',
      u'{virus}',
      u'{action0_map}',
      u'{action1_map}',
      u'{action2_map}']

  SOURCE_LONG = 'Symantec AV Log'
  SOURCE_SHORT = 'LOG'

  def GetMessages(self, unused_formatter_mediator, event_object):
    """Determines the formatted message strings for an event object.

    Args:
      formatter_mediator: the formatter mediator object (instance of
                          FormatterMediator).
      event_object: the event object (instance of EventObject).

    Returns:
      A tuple containing the formatted message string and short message string.

    Raises:
      WrongFormatter: if the event object cannot be formatted by the formatter.
    """
    if self.DATA_TYPE != event_object.data_type:
      raise errors.WrongFormatter(u'Unsupported data type: {0:s}.'.format(
          event_object.data_type))

    event_values = event_object.GetValues()

    event = event_values.get(u'event', None)
    if event:
      event_values[u'event_map'] = self.EVENT_NAMES.get(event, u'Unknown')

    category = event_values.get(u'cat', None)
    if category:
      event_values[u'category_map'] = self.CATEGORY_NAMES.get(
          category, u'Unknown')

    action = event_values.get(u'action0', None)
    if action:
      event_values[u'action0_map'] = self.ACTION_0_NAMES.get(action, u'Unknown')

    action = event_values.get(u'action1', None)
    if action:
      event_values[u'action1_map'] = self.ACTION_1_2_NAMES.get(
          action, u'Unknown')

    action = event_values.get(u'action2', None)
    if action:
      event_values[u'action2_map'] = self.ACTION_1_2_NAMES.get(
          action, u'Unknown')

    return self._ConditionalFormatMessages(event_values)


manager.FormattersManager.RegisterFormatter(SymantecFormatter)
