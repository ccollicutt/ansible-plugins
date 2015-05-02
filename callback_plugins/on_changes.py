import os
import urllib
import urllib2
import ConfigParser
import socket
import sys
try:
    from slacker import Slacker
except:
    print "ERROR: Callback plugin requires slacker, pip install slacker"
    sys.exit(1)

from ansible import utils

class CallbackModule(object):
    """
    Do something on changes
    """

    def __init__(self):
        self.read_settings()
        self.slack = Slacker(self.api_token)
        self.hostname = socket.gethostname()

    def read_settings(self):
        ''' Reads the settings from the on_changes.ini file '''
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.dirname(os.path.realpath(__file__)) + '/on_changes.ini')

        config_options = ['api_token', 'channel']
        for option in config_options:
          value = None
          if config.has_option('slack', option):
              value = config.get('slack', option)
          setattr(self, option, value)

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        pass

    def runner_on_ok(self, host, res):
        pass

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        pass

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        pass

    def runner_on_async_ok(self, host, res, jid):
        pass

    def runner_on_async_failed(self, host, res, jid):
        pass

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                encrypt=None, confirm=False, salt_size=None,
                                salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, name):
        self.playbook_name, _ = os.path.splitext(
         os.path.basename(self.play.playbook.filename))

    def playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())
        changes = False
        for h in hosts:
            s = stats.summarize(h)

            if s['changed'] > 0:
              print "INFO: %s has changes" % h
              changes = True

        if changes:
            msg = ":red_circle: _%s_ - %s playbook caused changes" % \
            (self.hostname, self.playbook_name)
        else:
            msg = ":smiley: _%s_ - %s playbook ran with no changes" % \
            (self.hostname, self.playbook_name)

        self.send_msg(msg)

    def send_msg(self, msg):
        try:
            self.slack.chat.post_message(self.channel, msg)
        except:
            print "ERROR: Failed to post message to slack"
