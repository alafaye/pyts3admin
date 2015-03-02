import argparse
import pyts3admin

parser = argparse.ArgumentParser()
parser.add_argument("yaml", help="Target yaml file to use")
parser.add_argument("--password", help="To specify password")
args = parser.parse_args()

if args.password:
    ts = pyts3admin.AdminSession(password=args.password)
else:
    print("You need to specify a password  for an admin session \
          with --password")

for vid in ts.virtual_server_ids():
    ts.choose_virtual_server(vid)
    ts.deploy_chans(args.yaml)
