import pandas as pd
import random
from string import ascii_lowercase
from sklearn.preprocessing import LabelEncoder

def create_dataset(filename):
	
	print("Creating pseudo labelled data...\n")
	data_array = pd.read_csv(filename, delimiter=',')
	data_array['real_password'] = 'password22'
	data_array['brute_force'] = 1

	legit = pd.DataFrame(columns= ['username', 'passwords', 'real_password', 'brute_force'])

	for x in range(2000):
		# randomize all letters, same length
		passwords = "".join(random.choice(ascii_lowercase) for i in range(10))
		real_length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(real_length))
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	for x in range(2000):
		# add an extra character to the end of the password
		length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(length))
		passwords = real_password + random.choice(ascii_lowercase)
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	for x in range(2000):
		# change a random character in the password to another
		length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(length))
		char = random.choice(ascii_lowercase)
		pos = random.randrange(0, length-1)
		pass_list = list(real_password)
		pass_list[pos] = char
		passwords = ''.join(pass_list)
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	for x in range(1000):
		# one wrong character and an extra character
		length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(length))
		char = random.choice(ascii_lowercase)
		pos = random.randrange(0, length-1)
		pass_list = list(real_password)
		pass_list[pos] = char
		passwords = ''.join(pass_list) + random.choice(ascii_lowercase)
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	for x in range(1000):
		# two wrong letters
		length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(length))
		char0 = random.choice(ascii_lowercase)
		char1 = random.choice(ascii_lowercase)
		pos0 = random.randrange(0, length-1)
		pos1 = random.randrange(0, length-1)
		while(pos0 == pos1):
			pos1 = random.randrange(0, length-1)
		pass_list = list(real_password)
		pass_list[pos0] = char0
		pass_list[pos1] = char1
		passwords = ''.join(pass_list)
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	for x in range(2000):
		# missing letter
		length = random.randrange(5, 15, 1)
		real_password = "".join(random.choice(ascii_lowercase) for i in range(length))	
		index = random.randint(0, length-1)
		passwords = real_password[:index] + real_password[index+1:]
		legit = legit.append({'username' : 'username', 'passwords' : passwords, 'real_password' : real_password, 'brute_force' : 0}, ignore_index=True)

	final_dataset = pd.concat([data_array, legit], ignore_index=True)
	final_dataset = final_dataset.sample(frac=1).reset_index(drop=True)
	
	return final_dataset


def feature_engineering(final_dataset):
	
	print('Starting Feature Engineering...\n')
	
	# Numerical feature - Difference in length between attempted password and real password
	final_dataset['length_diff'] = final_dataset['real_password'].str.len() - final_dataset['passwords'].str.len()
	
	# Boolean feature - True if username and attempted password are the same
	final_dataset.loc[final_dataset['username']==final_dataset['passwords'], 'user_pass_match'] = True
	final_dataset.loc[final_dataset['username']!=final_dataset['passwords'], 'user_pass_match'] = False
	
	
	# Numerical feature - number of incorrect characters in attempted password
	final_dataset.passwords = final_dataset.passwords.astype(str)
	final_dataset['incorrect_chars'] = 0
	for x in final_dataset.index:
		counter = 0
		iter = 0
		str1 = final_dataset['real_password'][x]
		str2 = final_dataset['passwords'][x]
		real_list = list(str1)
		other_list = list(str2)
		if final_dataset['length_diff'][x] < 0:
			iter = len(str1)
		else:
			iter = len(str2)
		for i in range(iter):
			if real_list[i] != other_list[i]:
				counter+=1
		total_diff = counter + abs(final_dataset['length_diff'][x])

		final_dataset['incorrect_chars'][x] = total_diff 
	
	return final_dataset

def preprocessing(final_dataset):

	print('Starting Preprocessing...\n')
	le = LabelEncoder().fit(final_dataset.username)
	final_dataset.username = le.transform(final_dataset.username)
	
	le = LabelEncoder().fit(final_dataset.passwords)
	final_dataset.passwords = le.transform(final_dataset.passwords)
	
	le = LabelEncoder().fit(final_dataset.real_password)
	final_dataset.real_password = le.transform(final_dataset.real_password)
	
	return final_dataset.dropna()