# A separate file is saved for every individual algorithm, but samples themselves are overwritten

import os 
import time
import datetime

num_samples = int(input("Enter number of times to loop: \n"))

openssl_dir = os.path.expanduser('.')

def initCert(algorithm, bits = ''):
	algorithm0 = algorithm
	algorithm = algorithm.replace('-', '').replace('+', '')
	if algorithm == 'rsa':
		myCmd = f'{openssl_dir}/apps/openssl req -x509 -new -newkey rsa:{bits} -keyout certs/key_CA_{algorithm}{bits}.key -out certs/key_CA_{algorithm}{bits}.pem -pkeyopt certs/rsa_keygen_bits:{bits} -nodes -subj "/CN=oqstest CA" -days 365 -config {openssl_dir}/apps/openssl.cnf > /dev/null 2>&1'
		os.system(myCmd)
	if algorithm == 'secp':
		myCmd =f'{openssl_dir}/apps/openssl ecparam -out certs/key_CA_{algorithm}{bits}.key -name {algorithm}{bits} -genkey '
		os.system(myCmd)
		myCmd =f'{openssl_dir}/apps/openssl req -new -key certs/key_CA_{algorithm}{bits}.key -x509 -nodes -days 365 -out certs/key_CA_{algorithm}{bits}.pem -nodes -subj "/CN=oqstest CA" -days 365 -config {openssl_dir}/apps/openssl.cnf'
		os.system(myCmd)
	else:
		myCmd = f'{openssl_dir}/apps/openssl req -x509 -new -newkey {algorithm0} -keyout certs/key_CA_{algorithm}{bits}.key -out certs/key_CA_{algorithm}{bits}.pem -nodes -subj "/CN=oqstest CA" -days 365 -config {openssl_dir}/apps/openssl.cnf > /dev/null 2>&1'
		os.system(myCmd)

def genKey(algorithm, num_samples, bits = ''):
	algorithm0 = algorithm
	algorithm = algorithm.replace('-', '').replace('+', '')
	if algorithm == 'rsa':
		myCmd = f'{openssl_dir}/apps/openssl genpkey -algorithm rsa -out certs/key_srv_{algorithm}{bits}.key -pkeyopt certs/rsa_keygen_bits:{bits} > /dev/null 2>&1'
		for i in range (num_samples):
			os.system(myCmd)
	if algorithm == 'secp':
		myCmd =f'{openssl_dir}/apps/openssl ecparam -out certs/key_srv_{algorithm}{bits}.key -name secp{bits} -genkey'
		for i in range(num_samples):
			os.system(myCmd)
	else:
		myCmd = f'{openssl_dir}/apps/openssl genpkey -algorithm {algorithm0} -out certs/key_srv_{algorithm}{bits}.key > /dev/null 2>&1'
		for i in range (num_samples):
			os.system(myCmd)

def genCSR(algorithm, num_samples, bits = ''):
	algorithm0 = algorithm
	algorithm = algorithm.replace('-', '').replace('+', '')
	if algorithm == 'rsa':
		myCmd = f'{openssl_dir}/apps/openssl req -new -key certs/key_srv_{algorithm}{bits}.key -out certs/key_srv_{algorithm}{bits}.csr -nodes -pkeyopt certs/rsa_keygen_bits:{bits} -subj \'/CN=oqstest server\' -config {openssl_dir}/apps/openssl.cnf > /dev/null 2>&1'
		for i in range (num_samples):
			os.system(myCmd)
	if algorithm == 'secp':
		myCmd =f'{openssl_dir}/apps/openssl req -newkey ec:certs/key_CA_{algorithm}{bits}.key -keyout certs/ec_PRIVATEKEY.key -out certs/key_srv_{algorithm}{bits}.csr -nodes -subj \'/CN=oqstest server\' -config {openssl_dir}/apps/openssl.cnf'
		for i in range (num_samples):
			os.system(myCmd)
	else:
		myCmd = f'{openssl_dir}/apps/openssl req -new -key certs/key_srv_{algorithm}{bits}.key -out certs/key_srv_{algorithm}{bits}.csr -nodes -subj \'/CN=oqstest server\' -config {openssl_dir}/apps/openssl.cnf > /dev/null 2>&1'
		for i in range (num_samples):
			os.system(myCmd)

def genCert(algorithm, num_samples, bits =''):
	algorithm0 = algorithm
	algorithm = algorithm.replace('-', '').replace('+', '')
	if algorithm == 'secp':
		myCmd=f'{openssl_dir}/apps/openssl x509 -req -in certs/key_srv_{algorithm}{bits}.csr -out certs/key_crt_{algorithm}{bits}.pem -CA certs/key_CA_{algorithm}{bits}.pem -CAkey certs/key_CA_{algorithm}{bits}.key -CAcreateserial -days 365'
		for i in range (num_samples):
			os.system(myCmd)
	else:
		myCmd = f'{openssl_dir}/apps/openssl x509 -req -in certs/key_srv_{algorithm}{bits}.csr -out certs/key_crt_{algorithm}{bits}.pem -CA certs/key_CA_{algorithm}{bits}.pem -CAkey certs/key_CA_{algorithm}{bits}.key -CAcreateserial -days 365' 
		for i in range (num_samples):
			os.system(myCmd)



def certVerify(algorithm, num_samples, bits = ''):
	algorithm0 = algorithm
	algorithm = algorithm.replace('-', '').replace('+', '')
	if algorithm == 'secp':
		myCmd = f'{openssl_dir}/apps/openssl verify -CAfile certs/key_CA_{algorithm}{bits}.pem certs/key_crt_{algorithm}{bits}.pem certs/key_crt_{algorithm}{bits}.pem'
		for i in range (num_samples):
			os.system(myCmd)
	else:
		myCmd = f'{openssl_dir}/apps/openssl verify -CAfile certs/key_CA_{algorithm}{bits}.pem certs/key_crt_{algorithm}{bits}.pem certs/key_crt_{algorithm}{bits}.pem'
		for i in range (num_samples):
			os.system(myCmd)


algorithms = [
	'secp','rsa','dilithium2','dilithium3','dilithium5', 'falcon512', 'falcon1024', 'SPHINCS+-SHA2-128f-simple', 'SPHINCS+-SHA2-128f-simple', 'SPHINCS+-SHA2-128s-simple', 'SPHINCS+-SHA2-192f-simple', 'SPHINCS+-SHA2-192s-simple', 'SPHINCS+-SHA2-256f-simple', 'SPHINCS+-SHA2-256s-simple', 'SPHINCS+-SHAKE-128f-simple', 'SPHINCS+-SHAKE-128s-simple', 'SPHINCS+-SHAKE-192f-simple', 'SPHINCS+-SHAKE-192s-simple', 'SPHINCS+-SHAKE-256f-simple', 'SPHINCS+-SHAKE-256s-simple'
]
algorithms_in_english = [
	'ECDSA','RSA', 'Dilithium 2', 'Dilithium 3', 'Dilithium 5', 'Falcon 512', 'Falcon 1024', 'SPHINCS+-SHA2-128f-simple', 'SPHINCS+-SHA2-128f-simple', 'SPHINCS+-SHA2-128s-simple', 'SPHINCS+-SHA2-192f-simple', 'SPHINCS+-SHA2-192s-simple', 'SPHINCS+-SHA2-256f-simple', 'SPHINCS+-SHA2-256s-simple', 'SPHINCS+-SHAKE-128f-simple', 'SPHINCS+-SHAKE-128s-simple', 'SPHINCS+-SHAKE-192f-simple', 'SPHINCS+-SHAKE-192s-simple', 'SPHINCS+-SHAKE-256f-simple', 'SPHINCS+-SHAKE-256s-simple'
]

#algorithms = [
#	'rsa','rsa3072_rainbowIcompressed','rsa3072_dilithium2'
#]
#algorithms_in_english = [
#	'RSA','RSA 3072 + Rainbow I Compressed','RSA 3072 + Dilithium2'
#]

def header():
	line = 'Timestamp,'
	line += 'Timestamp (Seconds),'
	line += 'Algorithm,'
	line += 'Algorithm (human readable),'
	line += 'Avg Key Gen Time (ms),'
	line += 'Avg Cert Signing Request Time (ms),'
	line += 'Avg Cert Gen Time (ms),'
	line += 'Avg Cert Verifying Time (ms),'
	return line

def run(file):
	rsa_bits_array = [2048, 3072, 4096];
	ecdsa_bits_array = ['256r1','384r1','521r1'];
	
	for i, algorithm in enumerate(algorithms):
		algorithm_in_english = algorithms_in_english[i]

		if algorithm == 'rsa':
			for bits in rsa_bits_array:
				print(f'Starting {algorithm} {bits}...')
				initCert(algorithm, bits)

				t1 = time.time()
				genKey(algorithm, num_samples, bits)
				t2 = time.time()
				avg_key_gen_time = (t2 - t1) / num_samples * 1000
				print('Key generation time: ')
				print(avg_key_gen_time)

				t1 = time.time()
				genCSR(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_signing_request_time = (t2 - t1) / num_samples * 1000
				print('CSR generation time')
				print(avg_cert_signing_request_time)

				t1 = time.time()
				genCert(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_gen_time = (t2 - t1) / num_samples * 1000
				print('Certificate generation time')
				print(avg_cert_gen_time)

				t1 = time.time()
				certVerify(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_verify_time = (t2 - t1) / num_samples * 1000
				print('Certificate verifying time')
				print(avg_cert_verify_time)

				now = datetime.datetime.now()
				time_end = (now - datetime.datetime(1970, 1, 1)).total_seconds()
				line = f'{now},{time_end},{algorithm} {bits},{algorithm_in_english} {bits},{avg_key_gen_time},{avg_cert_signing_request_time},{avg_cert_gen_time},{avg_cert_verify_time},'
				file.write(line + '\n')

		if algorithm == 'secp':
			for bits in ecdsa_bits_array:
				print(f'Starting {algorithm} {bits}...')
				initCert(algorithm, bits)

				t1 = time.time()
				genKey(algorithm, num_samples, bits)
				t2 = time.time()
				avg_key_gen_time = (t2 - t1) / num_samples * 1000
				print('Key generation time: ')
				print(avg_key_gen_time)

				t1 = time.time()
				genCSR(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_signing_request_time = (t2 - t1) / num_samples * 1000
				print('CSR generation time')
				print(avg_cert_signing_request_time)

				t1 = time.time()
				genCert(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_gen_time = (t2 - t1) / num_samples * 1000
				print('Certificate generation time')
				print(avg_cert_gen_time)

				t1 = time.time()
				certVerify(algorithm, num_samples, bits)
				t2 = time.time()
				avg_cert_verify_time = (t2 - t1) / num_samples * 1000
				print('Certificate verifying time')
				print(avg_cert_verify_time)

				now = datetime.datetime.now()
				time_end = (now - datetime.datetime(1970, 1, 1)).total_seconds()
				line = f'{now},{time_end},{algorithm} {bits},{algorithm_in_english} {bits},{avg_key_gen_time},{avg_cert_signing_request_time},{avg_cert_gen_time},{avg_cert_verify_time},'
				file.write(line + '\n')



		else:
			print(f'Starting {algorithm}...')
			initCert(algorithm)

			t1 = time.time()
			genKey(algorithm, num_samples)
			t2 = time.time()
			avg_key_gen_time = (t2 - t1) / num_samples * 1000
			print('Key generation time: ')
			print(avg_key_gen_time)

			t1 = time.time()
			genCSR(algorithm, num_samples)
			t2 = time.time()
			avg_cert_signing_request_time = (t2 - t1) / num_samples * 1000
			print('CSR generation time: ')
			print(avg_cert_signing_request_time)

			t1 = time.time()
			genCert(algorithm, num_samples)
			t2 = time.time()
			avg_cert_gen_time = (t2 - t1) / num_samples * 1000
			print('Certificate generation time')
			print(avg_cert_gen_time)

			t1 = time.time()
			certVerify(algorithm, num_samples)
			t2 = time.time()
			avg_cert_verify_time = (t2 - t1) / num_samples * 1000
			print('Certificate verifying time')
			print(avg_cert_verify_time)
			
			now = datetime.datetime.now()
			time_end = (now - datetime.datetime(1970, 1, 1)).total_seconds()
			line = f'{now},{time_end},{algorithm},{algorithm_in_english},{avg_key_gen_time},{avg_cert_signing_request_time},{avg_cert_gen_time},{avg_cert_verify_time},'
			file.write(line + '\n')




fileName = 'certs/NEW_LOGGED_OPENSSL_FINAL.csv'
file = open(fileName, 'w')
file.write(header() + '\n')
run(file)