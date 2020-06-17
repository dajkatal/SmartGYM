# Smart GYM

A Machine Learning-based program that can classify a teacher or a student in an open environment.

## Installation

Clone the directory to your computer and create a [virtual environment](https://djangocentral.com/how-to-a-create-virtual-environment-for-python/).
```sh
$ cd (Location of directory)
$ pip install -r requirements.txt
$ cd smart_gym
$ python manage.py runserver
```

## Seting up a new user

New users can be added from the localhost webpage. A webcam will open and the user will need to rotate their head to get full coverage of their face. 
- (When enough data is collected, press Q to close the webcam)

[The  data is stored in this [text file](https://github.com/dajkatal/SmartGYM/blob/master/smart_gym/home/facerecognition/facerec_128D.txt).]

## Face recognition app

Steps to run the facial recognition script:
```sh
$ cd (Location of directory)
$ cd smart_gym/home/facerecognition
$ python main.py
```
* To terminate main.py, press Q

## Processing Information
All of the data gathered from the facial recognition model is logged into a [csv file](https://github.com/dajkatal/SmartGYM/blob/master/smart_gym/home/facerecognition/current.csv).

<table>
	<caption>(The format of the CSV file)</caption>
	<tr>
		<th>People in the GYM</th><th>
		</th><th></th>
		<th>Teacher Around</th> <th>Time</th>
	</tr>
	<tr>
		<td>Name</td>
		<td>Time</td>
		<td>Flag</td>
		<td>Yes/No</td>
		<td>0</td>
	</tr>
</table>
* Flags change color based on the time a student has been in frame.
