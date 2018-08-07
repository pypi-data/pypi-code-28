"""

Help Menu
    Help menu object containing body of help content.
    For printing with formatting

"""

from pyaws.core.colors import Colors

PACKAGE = 'machineimage'
PKG_ACCENT = Colors.ORANGE
PARAM_ACCENT = Colors.WHITE
AMI = Colors.DARKCYAN
RESET = Colors.RESET

synopsis_cmd = (
    Colors.RESET + PKG_ACCENT + Colors.BOLD + PACKAGE + RESET +
    PARAM_ACCENT + '  --image ' + Colors.RESET + '{' + AMI + 'OS_TYPE' + RESET + '}' +
    PARAM_ACCENT + '  --profile' + Colors.RESET + ' <value>' +
    PARAM_ACCENT + '  --region' + Colors.RESET + ' <value>'
    )

url_sc = Colors.URL + 'https://github.com/fstab50/ec2tools' + Colors.RESET

menu_body = Colors.BOLD + Colors.WHITE + """
  DESCRIPTION""" + Colors.RESET + """

            Return latest Amazon Machine Image (AMI) in a Region
            Source Code:  """ + url_sc + """
    """ + Colors.BOLD + Colors.WHITE + """
  SYNOPSIS""" + Colors.RESET + """

          """ + synopsis_cmd + """

                            -i, --image   <value>
                           [-d, --details  ]
                           [-n, --filename <value> ]
                           [-f, --format   <value> ]
                           [-p, --profile <value> ]
                           [-r, --region   <value> ]
                           [-d, --debug    ]
                           [-h, --help     ]
                           [-V, --version  ]
    """ + Colors.BOLD + Colors.WHITE + """
  OPTIONS
    """ + Colors.BOLD + """
        -i, --image""" + Colors.RESET + """ (string) : Amazon Machine Image Operating System type.
            Must be value from the following list.

                EC2 Amazon Machine Image (AMI) OS_TYPE:

                    - """ + AMI + """amazonlinux1""" + RESET + """    :   Amazon Linux v1 (2018)
                    - """ + AMI + """amazonlinux2""" + RESET + """    :   Amazon Linux v2 (2017.12+)
                    - """ + AMI + """centos5""" + RESET + """         :   CentOS 5 (RHEL 5+)
                    - """ + AMI + """centos6""" + RESET + """         :   CentOS 6 (RHEL 6+)
                    - """ + AMI + """centos7""" + RESET + """         :   CentOS 7 (RHEL 7+)
                    - """ + AMI + """redhat7.3""" + RESET + """       :   Redhat Enterprise Linux 7.3
                    - """ + AMI + """redhat7.4""" + RESET + """       :   Redhat Enterprise Linux 7.4
                    - """ + AMI + """redhat7.5""" + RESET + """       :   Redhat Enterprise Linux 7.5
                    - """ + AMI + """ubuntu14.04""" + RESET + """     :   Ubuntu Linux 14.04
                    - """ + AMI + """ubuntu16.04""" + RESET + """     :   Ubuntu Linux 16.04
                    - """ + AMI + """ubuntu18.04""" + RESET + """     :   Ubuntu Linux 18.04
    """ + Colors.BOLD + Colors.WHITE + """
        -p, --profile""" + Colors.RESET + """ (string) : Profile name of an IAM user from the local
            awscli configuration to  be  used when authenticating to Amazon
            Web Services. If omitted, defaults to "default" profilename.
    """ + Colors.BOLD + Colors.WHITE + """
        -d, --details""" + Colors.RESET + """ : Output all metadata associated with each individual
            Amazon Machine Image identifier returned.
    """ + Colors.BOLD + Colors.WHITE + """
        -f, --format""" + Colors.RESET + """ (string):  Output format, json or  plain text (DEFAULT:
            json).
    """ + Colors.BOLD + Colors.WHITE + """
        -n, --filename""" + Colors.RESET + """ <value>:  Write output to a filesystem object with a
            name specified in the --filename parameter.
    """ + Colors.BOLD + Colors.WHITE + """
        -r, --region""" + Colors.RESET + """ <value>: Amazon Web Services Region Code. When provided
            as a parameter, """ + PACKAGE + """ returns  the AMI  image only for  a
            particular AWS region.  Examples: ap-northeast-1 (Tokyo, Japan).
            If region omitted, returns Amazon Machine Images for all regions.
    """ + Colors.BOLD + Colors.WHITE + """
        -d, --debug""" + Colors.RESET + """ :  Turn on verbose log output.
    """ + Colors.BOLD + Colors.WHITE + """
        -V, --version""" + Colors.RESET + """ : Print package version.
    """ + Colors.BOLD + Colors.WHITE + """
        -h, --help""" + Colors.RESET + """ : Show this help message and exit.

    """
