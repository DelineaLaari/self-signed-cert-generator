# Self-Signed Certificate Generator

The **Self-Signed Certificate Generator** repository contains a Python script to create self-signed certificates with support for `subjectAltName` and `commonName`. This tool allows the generation of certificates in both P12 and PFX formats and provides an easy-to-use configuration file to customize certificate attributes.

## Use Cases
- Secure local development environments.
- Test HTTPS setups without the need for a CA-signed certificate. E.g. IWA testing.
- Create custom certificates for internal applications.

## Features
- Generate private keys and self-signed certificates.
- Support for `subjectAltName` (SAN) and `commonName` (CN).
- Create certificates in P12 or PFX formats.
- Easy configuration through a dedicated `config.py` file.
- Customizable certificate directory and file names.
- Password protection for P12/PFX certificates.

## Prerequisites
- Python 3.x
- OpenSSL installed on your system

## Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/self-signed-cert-generator.git
   cd self-signed-cert-generator

2. Configure the certificate settings in config.py.
- **CERT_DIR**: Directory to store the generated certificate files.
- **PRIVATE_KEY**: Filename for the private key.
- **CSR**: Filename for the Certificate Signing Request.
- **CERTIFICATE**: Filename for the generated certificate.
- **P12_CERTIFICATE**: Filename for the P12/PFX certificate.
- **P12_PASSWORD**: Password for the P12/PFX certificate.
- **DAYS_VALID**: Number of days the certificate will be valid.
- **ALT_NAMES**: Subject Alternative Names (SAN) for the certificate.
- **SUBJECT_NAME**: Distinguished Name for the certificate.

## Usage
1. Run the script to generate a certificate:
   ```bash
   python generate_certificate.py --format p12

2. Parameters:
   ```plaintext
   --format: The format of the certificate to generate (p12 or pfx). The default is p12.
   --cert-dir: Directory to store the generated certificate files. The default is certificates.

## Troubleshooting
If you encounter any issues, please check the following:
- Ensure the `config.py` file is correctly configured.
- Verify that you have the necessary permissions to create files in the specified directory.
- Check for any errors in the output log and address them accordingly.
- If Chrome shows "Not Secure" beside the URL even after generating and installing the certificate, ensure the following:
  - The `subjectAltName` field is included in the certificate.
  - The certificate is installed in the Trusted Root Certification Authorities store.
  - The browser cache is cleared.


> **Note:** If you keep getting prompted for username/password when using IWA.
> - Open the internet properties on the taskbar and select security.
> - Choose Internet click custom level. You’ll find user authentication at the bottom of the list.
> - Change the policy to automatic logon with current username and password.
