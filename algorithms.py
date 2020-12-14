from math import sqrt
from sklearn import metrics
from statistics import mean
from preprocess_data import preprocessing 
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid

def split_train_predict(model, final_dataset, final_y):
	X_train, X_test, y_train, y_test = train_test_split(final_dataset, final_y, test_size=0.2)
	model.fit(X_train, y_train)
	pred_y = model.predict(X_test)
	print("\nAccuracy:",metrics.accuracy_score(y_test, pred_y))
	print("Precision:",metrics.precision_score(y_test, pred_y))
	return pred_y

def linear_svc(final_dataset, final_y):
	# Linear SVC Model
	invalid = True
	while (invalid):
		c = input("Enter a value for c:\n")
		try:
			c = float(c)
			if c > 0:
				invalid = False
			else:	
				print(" - Please enter a positive value - \n")
		except ValueError:
			print(" - Please enter a number - \n")
	invalid = True
	while (invalid):
		m = input("Enter a value for max_iter:\n")
		try:
			m = int(m)
			if c > 0:
				invalid = False
			else:	
				print(" - Please enter a positive value - \n")
		except ValueError:
			print(" - Please enter a number - \n")
	linear_svc = svm.LinearSVC(C=c, random_state=0, max_iter=m)
	linear_svc_rmse = sqrt(-1 * mean(cross_val_score(linear_svc, final_dataset, final_y, scoring='neg_mean_squared_error')))
	print("\nThe Root Mean Squared Error for \nLinear SVC is:",linear_svc_rmse,"\n")
	linear_svc_y = split_train_predict(linear_svc, final_dataset, final_y)

def rbf_svc(final_dataset, final_y):
	# RBF SVC Model
	invalid = True
	while (invalid):
		c = input("Enter a value for c:\n")
		try:
			c = float(c)
			if c > 0:
				invalid = False
			else:	
				print(" - Please enter a positive value - \n")
		except ValueError:
			print(" - Please enter a number - \n")
		
	svmm = svm.SVC(kernel='rbf', C=c)
	svm_rmse = sqrt(-1 * mean(cross_val_score(svmm, final_dataset, final_y, scoring='neg_mean_squared_error')))
	print("The Root Mean Squared Error for \nRBF SVC is:",svm_rmse,"\n")
	svm_y = split_train_predict(svmm, final_dataset, final_y)

def sgd_classifier(final_dataset, final_y):
	# SGD Classifier Model
	invalid = True
	while (invalid):
		i = input("Enter a value for max iterations:\n")
		try:
			i = int(i)
			if i > 0:
				invalid = False
			else:	
				print(" - Please enter a positive value - \n")
		except ValueError:
			print(" - Please enter a number - \n")
	sgdc = SGDClassifier(max_iter=i)
	sgdc_rmse = sqrt(-1 * mean(cross_val_score(sgdc, final_dataset, final_y, scoring='neg_mean_squared_error')))
	print("The Root Mean Squared Error for \nSGD Classifier is:",sgdc_rmse,"\n")
	sgd_y = split_train_predict(sgdc, final_dataset, final_y)

def knn_classifier(final_dataset, final_y):
	# KNN Classifier
	invalid = True
	while (invalid):
		n = input("Enter a value for n:\n")
		try:
			n = int(n)
			if n > 0:
				invalid = False
			else:	
				print(" - Please enter a positive value - \n")
		except ValueError:
			print(" - Please enter a number - \n")
	knn = KNeighborsClassifier(n_neighbors=n)
	knn_rmse = sqrt(-1 * mean(cross_val_score(knn, final_dataset, final_y, scoring='neg_mean_squared_error')))
	print("The Root Mean Squared Error for \nKNN Classifier is:",knn_rmse,"\n")	
	knn_y = split_train_predict(knn, final_dataset, final_y)

def nearest_centroid(final_dataset, final_y):
	# NearestCentroid Classifier
	centroid = NearestCentroid()
	centroid_rmse = sqrt(-1 * mean(cross_val_score(centroid, final_dataset, final_y, scoring='neg_mean_squared_error')))
	print("The Root Mean Squared Error for \nNearest Centroid Classifier is:",centroid_rmse,"\n")
	centroid_y = split_train_predict(centroid, final_dataset, final_y)

def choose_algorithm(final_dataset, final_y):
	algorithms = {
		"1": {"Linear SVC" : linear_svc},
		"2": {"RBF SVC" : rbf_svc},
		"3": {"SGD Classifier" : sgd_classifier},
		"4": {"KNearest Neighbors" : knn_classifier},
		"5": {"Nearest Centroid" : nearest_centroid},
		"6": {"Quit": "null"}
	}

	invalid_algorithm = True
	while( invalid_algorithm ):
		print('\nAlgorithms :')
		for key, value in algorithms.items():
			for name,  func in value.items():
				print(key," : ",name)
		choice = input("\nChoose an algorithm to run on the dataset:\n")
		try:
			if int(choice) == 6:
				invalid_algorithm = False
			elif choice in algorithms:
				invalid_algorithm = False
				d = algorithms.get(choice, {})
				func = next(iter(d.values()))
				func(final_dataset, final_y)
			else:
				print("Invalid choice - please select again\n")
		except ValueError:
			print("Please enter a number from the list shown\n")
