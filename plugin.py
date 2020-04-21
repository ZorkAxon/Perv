###
# Copyright (c) 2020, Zork
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import random
import re
import pickle
import supybot.world as world
from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
from supybot import conf
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Perv')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

filename = conf.supybot.directories.data.dirize("Perv.db")

class Perv(callbacks.Plugin):
    """A collection of funny "perverted" triggers for my Axon friends."""


    def loadDB(self):
        try:
            with open(filename, rb) as f:
                self.db = pickle.load(f)
        except Exception as e:
            self.log.debug('Perv: Unable to load pickled database %s', e)

    def exportDB(self):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.db, f, 2)
        except Exception as e:
            self.log.warning('Perv: Unable to write pickled database: %s', e)

    def __init__(self, irc):
        self.__parent = super(Perv, self)
        self.__parent.__init__(irc)
        self.defaultdb = {'JIZZED' : 0}
        self.db = self.defaultdb
        self.loadDB()
        world.flushers.append(self.exportDB)

    def die(self):
        self.exportDB()
        world.flushers.remove(self.exportDB)
        self.__parent.die()




    @wrap(['nick'])
    def jizz (self, irc, msg, args, nick):
        """<nick>
        """
#        For Debugging
#        irc.reply('Trigger Working')
        rnick =  random.choice(list(irc.state.channels[msg.channel].users))
        nick = nick
        jizzed = self.db['JIZZED']
        var = jizzed + 1
        self.db['JIZZED'] = var


        outcomes = {
            "Starts pumping his peen... CUMS all over %s" % (nick),
            "Starts pumping his peen... Prematurely ejaculates! This never happends baby!!",
            "Starts pumping his peen... Gets a cramp and falls on his back spraying jizz on everyone!",
            "Starts pumping his peen... Misses %s! Instead CUMS all over %s face" % (nick, rnick),
            "Starts pumping his peen... BLOWS a giant load into %s ear" % (nick),
        }

        output = random.choice(list(outcomes))
        joutput = "I have jizzed %s times" % var
        self.exportDB()


        if nick != rnick:
            irc.reply(output, action=True)
            irc.reply(joutput)
        else:
            txt = "Starts pumping his peen... Prematurely ejaculates! This never happends baby!!"
            irc.reply(txt, action=True)
            irc.reply(joutput)
    pass

Class = Perv


    # vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

