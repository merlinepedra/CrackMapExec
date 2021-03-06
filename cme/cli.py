# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter
from cme.loaders.protocol_loader import protocol_loader
from cme.helpers.logger import highlight


class MyArgumentParser(ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()


class MyFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    pass


def gen_cli_args():

    VERSION = '4.1.0dev'
    CODENAME = u'ҪФԠЯДDЄ ԐDЇҐЇФЍ'

    p_loader = protocol_loader()
    protocols = p_loader.get_protocols()

    parser = MyArgumentParser(description=u"""
      ______ .______           ___        ______  __  ___ .___  ___.      ___      .______    _______ ___   ___  _______   ______
     /      ||   _  \         /   \      /      ||  |/  / |   \/   |     /   \     |   _  \  |   ____|\  \ /  / |   ____| /      |
    |  ,----'|  |_)  |       /  ^  \    |  ,----'|  '  /  |  \  /  |    /  ^  \    |  |_)  | |  |__    \  V  /  |  |__   |  ,----'
    |  |     |      /       /  /_\  \   |  |     |    <   |  |\/|  |   /  /_\  \   |   ___/  |   __|    >   <   |   __|  |  |
    |  `----.|  |\  \----. /  _____  \  |  `----.|  .  \  |  |  |  |  /  _____  \  |  |      |  |____  /  .  \  |  |____ |  `----.
     \______|| _| `._____|/__/     \__\  \______||__|\__\ |__|  |__| /__/     \__\ | _|      |_______|/__/ \__\ |_______| \______|

                                         A swiss army knife for pentesting networks
                                    Forged by @byt3bl33d3r using the powah of dank memes

                                                      {}: {}
                                                  {}: {}
""".format(highlight('Version', 'red'),
           highlight(VERSION),
           highlight('Codename', 'red'),
           highlight(CODENAME)),

                                    formatter_class=MyFormatter,
                                    version=u'{} - {}'.format(VERSION, CODENAME),
                                    fromfile_prefix_chars='@',
                                    epilog=u"ЇЍ SФVЇԐҬ ЯЦSSЇД, ҪЯДҪҚԠДPЭӾЭҪ ԠЇԠЇҠДҬZ'S ҰФЏ!")

    parser.add_argument("-t", type=int, dest="threads", default=100, help="set how many concurrent threads to use")
    parser.add_argument("--timeout", default=None, type=int, help='max timeout in seconds of each thread')
    parser.add_argument("--jitter", metavar='INTERVAL', type=str, help='sets a random delay between each connection')
    parser.add_argument("--darrell", action='store_true', help='give Darrell a hand')
    parser.add_argument("--verbose", action='store_true', help="enable verbose output")

    subparsers = parser.add_subparsers(title='protocols', dest='protocol', description='available protocols')

    std_parser = MyArgumentParser(add_help=False, fromfile_prefix_chars='@', formatter_class=MyFormatter)
    std_parser.add_argument("target", nargs='*', type=str, help="the target IP(s), range(s), CIDR(s), hostname(s), FQDN(s), file(s) containing a list of targets, NMap XML or .Nessus file(s)")
    std_parser.add_argument('-id', metavar="CRED_ID", nargs='+', default=[], type=str, dest='cred_id', help='database credential ID(s) to use for authentication')
    std_parser.add_argument("-u", metavar="USERNAME", dest='username', nargs='+', default=[], help="username(s) or file(s) containing usernames")
    std_parser.add_argument("-p", metavar="PASSWORD", dest='password', nargs='+', default=[], help="password(s) or file(s) containing passwords")
    fail_group = std_parser.add_mutually_exclusive_group()
    fail_group.add_argument("--gfail-limit", metavar='LIMIT', type=int, help='max number of global failed login attempts')
    fail_group.add_argument("--ufail-limit", metavar='LIMIT', type=int, help='max number of failed login attempts per username')
    fail_group.add_argument("--fail-limit", metavar='LIMIT', type=int, help='max number of failed login attempts per host')

    module_parser = MyArgumentParser(add_help=False, fromfile_prefix_chars='@', formatter_class=MyFormatter)
    mgroup = module_parser.add_mutually_exclusive_group()
    mgroup.add_argument("-M", "--module", metavar='MODULE', help='module to use')
    module_parser.add_argument('-o', metavar='MODULE_OPTION', nargs='+', default=[], dest='module_options', help='module options')
    module_parser.add_argument('-L', '--list-modules', action='store_true', help='list available modules')
    module_parser.add_argument('--options', dest='show_module_options', action='store_true', help='display module options')

    for protocol in protocols.keys():
        protocol_object = p_loader.load_protocol(protocols[protocol]['path'])
        subparsers = getattr(protocol_object, protocol).proto_args(subparsers, std_parser, module_parser)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args
