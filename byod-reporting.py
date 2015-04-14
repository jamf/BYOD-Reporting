import argparse
import base64
import csv
import datetime
import getpass
import os
import sys
import urllib2
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree


class JSS(object):
    def __init__(self, url, username, password):
        self.auth = "Basic {}".format(base64.b64encode(username + ':' + password))
        self.server = url + '/JSSResource'

    def get_mobile_device(self, serial_num):
        request_url = '{}/mobiledevices/serialnumber/{}/subset/General&Location'.format(self.server, serial_num)
        request = urllib2.Request(request_url)
        print("GET {}".format(request_url))
        return self.request(request)

    def request(self, request):
        request.add_header('Authorization', self.auth)
        request.add_header('Content-Type', 'text/xml')
        try:
            response = urllib2.urlopen(request)
        # except ValueError as e:
        #     print("an error occurred during the search: {0}".format(e.message))
        #     print("check the URL used and try again\n")
        #     sys.exit(1)
        except urllib2.HTTPError as e:
            print("{}: {}".format(e.code, e.reason))
            if e.code == 404:
                return False
            else:
                print("Response headers:\n{}".format(e.hdrs))
                print("Response text:\n{}".format(e.read()))
                print("Traceback:")
                sys.exit(1)
        except Exception as e:
            print("an unknown error has occurred: {}: {}\n".format(type(e).__name__, e.message))
            sys.exit(1)

        return response.read()


def device_list_from_csv(csv_file_path):
    """Returns a Python list of values from a single-column CSV file"""
    device_list = list()
    with open(csv_file_path, 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            device_list.append(urllib2.quote(row[0]))

    return device_list


def parse_args():
    parser = argparse.ArgumentParser(
            prog="BYO Reporting",
            description="Generate a CSV file of the eligibility status of BYO devices in the JSS.",
            formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""Example usage:
$ ./byo-reporting.py https://my.jss.com /path/to/serial-list.csv
            """)

    parser.add_argument('jssurl', type=str, help="JSS URL")
    parser.add_argument('input_file', type=str, help='Path to CSV device list')
    parser.add_argument('-o', '--output', type=str, dest='output_file', help="Path to write CSV (default current dir)",
                        default='{}/output.csv'.format(os.getcwd()))
    parser.add_argument('-u', '--username', dest='username', type=str, default=None, help="API username")
    parser.add_argument('-p', '--password', dest='password', type=str, default=None, help="API user password")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not args.username:
        args.username = str(raw_input("Enter the JSS user: "))

    if not args.password:
        args.password = getpass.getpass("Enter the password: ")

    return args


def days_since_last_update(unix_epoch):
    now = datetime.datetime.utcnow()
    last_update = datetime.datetime.fromtimestamp(float(unix_epoch) / 1000)
    return (now - last_update).days


def write_csv(data, file_path):
    with open(file_path, 'w') as f:
        print("Writing CSV file to: {}".format(f.name))
        csv_file = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csv_file.writerow(row)


def main():
    args = parse_args()
    input_list = device_list_from_csv(args.input_file)
    jss = JSS(args.jssurl, args.username, args.password)

    output_data = list()
    # CSV column headers
    output_data.append(['Name', 'Serial Number', 'Enrolled?', 'Last Update (days)', 'BYO Eligible?'])

    for serial_number in input_list:
        result = jss.get_mobile_device(serial_number)
        if result:
            row = list()
            root = etree.fromstring(result)
            row.append(root.findtext('location/real_name'))
            row.append(serial_number)
            row.append(root.findtext('general/managed'))
            row.append(days_since_last_update(root.findtext('general/last_inventory_update_epoch')))
            if row[2] != 'true' or int(row[3]) > 30:
                row.append('No: remove from BYO')

            else:
                row.append('Yes')

            output_data.append(row)
        else:
            print("Device {} not found, skipped".format(serial_number))

    write_csv(output_data, args.output_file)
    print("Done\n")


if __name__ == '__main__':
    main()