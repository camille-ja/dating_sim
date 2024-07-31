import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split #lets you split data into training/testing
import joblib #for saving a model
import random
import warnings
warnings.filterwarnings("ignore")

f_names = ["Sara", "Betty", "Georgia", "Peach", "Daisy", "Luna", "Echo", "Maribell"]
m_names = ["Jon", "Diego", "Carlos", "Joseph", "Andrew", "Rick", "Richard", "Louie"]


def Answers(response, choices, text):
    while choices.find(response.lower()) == -1:
        response = input(text)
    return response

#finds match based off music taste
def Matches(age_pref, gender_pref, music_pref, upgrade):
    if gender_pref == "a": #converts gender to number
        gender = random.randrange(0,2)
    elif gender_pref == "f":
        gender = 1
    else:
        gender = 0
        
    pool = pd.read_csv('music.csv') #grabs dating pool
    match = pool.drop(columns=['genre']) #age + gender
    gen = pool['genre']
    model = DecisionTreeClassifier()
    model.fit(match.values, gen)
    if upgrade:
        joblib.load('music-recommender.joblib')
        p = model.predict([[age_pref, gender]]) #predicts music taste baesd on age and gender
        prediction = p[0]
    else:
        prediction = "x"
    found = False
    while not found: #loops untill a partner is found that matches music taste (for upgrade)
        list = Partner(match, gen, gender)
        if prediction == "x" or prediction == list[3]:
            found = True
    return list
        
def Partner(match, gen, gender): #Finds random partner from dataset
    junk, partner, junk_two, partner_music = train_test_split(match, gen, test_size=0.01) #grabs one person from ds
    age_part = partner.iat[0,0]
    gender_part = partner.iat[0,1]
    music_part = partner_music.iat[0]
    if gender_part == 1:
        name_part = f_names[random.randrange(0, len(f_names))]
    else:
        name_part = m_names[random.randrange(0, len(m_names))]
    return [name_part, age_part, gender_part, music_part]

#ask for name and age and favorite music, connect w people of similar age, have them choose one person and see if they're combatible or no
print("Welcome to dating sim!")
name = input("Enter your name: ")
age = input("Enter your age: ")
print("Building profile...")
gender = Answers("c", "mfa", name + " is interested in dating... (male:m,female:f,anyone:a)")
music = Answers("w", "classicalhiphopjazzdanceacoustic", name + "'s favorite music genre is... (Classical, HipHop, Jazz, Dance, Acoustic)")

print("Finding matches...")
for i in range(10):
    print("*")
    
print(1," perfect match found!!")
print("Please upgrade to dating sim PRO* to see your perfect match!!")
print("*for $1599.99 a month not cancelable for 12 months. Perfect match does not guarntee of perfect compatibility")
a = input("Would you like to upgrade? y/n: ")
upgrade = True
if a == 'y':
    num = input("Enter your card number: ")
    if len(num) != 16 and len(num) != 19:
        upgrade = False
    input("Expiration Date:")
    cvc = input("CVC:")
    if len(cvc) != 3:
        upgrade = False
    input("Enter you full leagl name: ")
    if upgrade:
        print("Thank you for your purchase!!")
    else:
        print("Invalid card. Moving to free version")
else:
    upgrade = False
if not upgrade:
    print("Assigning random match")
        
match = Matches(age, gender, "x", upgrade)
print(name + ", your match is...")
if match[2] == 1:
    match_g = "female"
else:
    match_g = "male"
for i in range(3):
    print("*")
print("Name:", match[0], "  Age:", match[1], "  Gender:", match_g, "  Favorite Music:", match[3])

score = 0.0
if match[1] >= int(age) - 2 and match[1] <= int(age) + 2:
    score+=1.0
if gender == "f" and match[2] == 1:
    score+=1.0
elif gender == "m" and match[2] == 0:
    score += 1.0
elif gender == "a":
    score += 1.0
if match[3] == music:
    score+=1.0
score /= 3
score *= 100
print("Your compatibility with " + match[0] + " is " + '%.0f' % score + "%!")


