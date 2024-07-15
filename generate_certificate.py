import subprocess
import config
import argparse
import os
import tempfile

def run_openssl_command(command):
    """Run an OpenSSL command and handle errors."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command: {command}")
        print(e)
        exit(1)

def generate_private_key():
    """Generate a private key."""
    command = f"openssl genrsa -out {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)} 2048"
    run_openssl_command(command)
    print(f"Private key generated: {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)}")

def create_csr():
    """Create a Certificate Signing Request (CSR) with subjectAltName."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_conf:
        tmp_conf.write(f"""
[ req ]
default_bits       = 2048
default_keyfile    = {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)}
distinguished_name = req_distinguished_name
req_extensions     = req_ext

[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
countryName_default         = US
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = State
localityName                = Locality Name (eg, city)
localityName_default        = City
organizationName            = Organization Name (eg, company)
organizationName_default    = Organization
organizationalUnitName      = Organizational Unit Name (eg, section)
organizationalUnitName_default = OrganizationalUnit
commonName                  = Common Name (eg, YOUR name)
commonName_default          = {config.SUBJECT_NAME.split('/CN=')[1]}

[ req_ext ]
subjectAltName = {config.ALT_NAMES}
        """.encode())

        tmp_conf_path = tmp_conf.name

    command = f"openssl req -new -key {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)} -out {os.path.join(config.CERT_DIR, config.CSR)} -subj \"{config.SUBJECT_NAME}\" -config {tmp_conf_path}"
    run_openssl_command(command)
    os.remove(tmp_conf_path)
    print(f"CSR generated: {os.path.join(config.CERT_DIR, config.CSR)}")

def generate_certificate():
    """Generate a self-signed certificate with subjectAltName."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_conf:
        tmp_conf.write(f"""
[ req ]
default_bits       = 2048
default_keyfile    = {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)}
distinguished_name = req_distinguished_name
x509_extensions    = v3_ca

[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
countryName_default         = US
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = State
localityName                = Locality Name (eg, city)
localityName_default        = City
organizationName            = Organization Name (eg, company)
organizationName_default    = Organization
organizationalUnitName      = Organizational Unit Name (eg, section)
organizationalUnitName_default = OrganizationalUnit
commonName                  = Common Name (eg, YOUR name)
commonName_default          = {config.SUBJECT_NAME.split('/CN=')[1]}

[ v3_ca ]
subjectAltName = {config.ALT_NAMES}
        """.encode())

        tmp_conf_path = tmp_conf.name

    command = f"openssl x509 -req -days {config.DAYS_VALID} -in {os.path.join(config.CERT_DIR, config.CSR)} -signkey {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)} -out {os.path.join(config.CERT_DIR, config.CERTIFICATE)} -extfile {tmp_conf_path} -extensions v3_ca"
    run_openssl_command(command)
    os.remove(tmp_conf_path)
    print(f"Certificate generated: {os.path.join(config.CERT_DIR, config.CERTIFICATE)}")

def create_p12_or_pfx(format):
    """Create a P12 or PFX file based on the specified format."""
    extension = "p12" if format.lower() == "p12" else "pfx"
    command = f"openssl pkcs12 -export -out {os.path.join(config.CERT_DIR, config.P12_CERTIFICATE.replace('.p12', f'.{extension}'))} -inkey {os.path.join(config.CERT_DIR, config.PRIVATE_KEY)} -in {os.path.join(config.CERT_DIR, config.CERTIFICATE)} -password pass:{config.P12_PASSWORD}"
    run_openssl_command(command)
    print(f"{extension.upper()} certificate generated: {os.path.join(config.CERT_DIR, config.P12_CERTIFICATE.replace('.p12', f'.{extension}'))}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a P12 or PFX certificate.")
    parser.add_argument('--format', type=str, choices=['p12', 'pfx'], default='p12', help='The format of the certificate to generate (p12 or pfx).')
    parser.add_argument('--cert-dir', type=str, default='certificates', help='Directory to store certificate files.')
    args = parser.parse_args()

    config.CERT_DIR = args.cert_dir

    # Create the directory if it doesn't exist
    os.makedirs(config.CERT_DIR, exist_ok=True)

    generate_private_key()
    create_csr()
    generate_certificate()
    create_p12_or_pfx(args.format)
