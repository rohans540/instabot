'''
Project name: Instabot
Developer: Rohan sharma
'''
import requests                 #To make HTTP requests simpler and handy
import urllib                   #fetching/downloading data through URLs using urlretrieve
import ctypes                   #used to provide message boxes of different styles
import os                       #importing os modules for reading/opening files[user posts/images/videos etc]
from textblob import TextBlob   #to make sentimental analysis on comments of a post
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL = "https://api.instagram.com/v1/"
ACCESS_TOKEN = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"      #ACCESS_TOKEN




#==================================================START_BOT_METHOD============================================================

#Method name: start_bot
#Provides user with a menu from which user can select any option of his/her choice

def start_bot():

    show_menu = True
    while show_menu:


        print """\n\t\t   Welcome to Instabot
         
         Please select an option:
         
         
            1. Get your own details.
            2. Get details of any other user.
            3. Get your own recent post.
            4. Get other user's recent post.
            5. To like the recent post.
            6. Comment on recent post.
            7. Delete negative comments from my own recent post.
            8. Delete negative comments from other user's post.
            9. More options.
           10. Display comments froma user's post.
            0. Exit from Instabot.
        
        """

        choice = raw_input()

        if choice == "1":
            self_info()

        elif choice == "2":
            insta_uname = raw_input("Enter the username of the user:\n")

            get_user_info(insta_uname)

        elif choice == "3":
            get_own_post()

        elif choice == "4":
            insta_uname = raw_input("Enter the username of the user:\n")
            get_user_post(insta_uname)

        elif choice == "5":
            insta_uname = raw_input("Enter the username of the user:\n")

            like_a_post(insta_uname)

        elif choice == "6":

            insta_uname = raw_input("Enter the username of the user:\n")

            comment_on_post(insta_uname)

        elif choice == "7":
            delete_neg_comments_self()

        elif choice == "8":
            insta_uname = raw_input("Enter the username of the user:\n")

            delete_neg_comments_user(insta_uname)

        elif choice == "9":
            more_options()

        elif choice == "10":
            insta_uname = raw_input("Enter the uisername of the user:\n")

            fetch_all_comments_user(insta_uname)

        elif choice == "0":

            print "Thank you for using instabot\nLogging out... All changes saved..\n"
            show_menu = False

        else:
            print "Oooops! you've entered a wrong input.. please try again"


    #================================================Message_box method===============================================

    def message_box(text, title, style):
        return ctypes.windll.user32.MessageBoxA(0, text, title, style)


    #===================================================SELF_INFO METHOD=============================================
    def self_info():

        request_url = (BASE_URL + "users/self/?access_token=%s") %ACCESS_TOKEN
        print "GET request url: %s" %request_url

        user_info = requests.get(request_url).json()

        if user_info["meta"]["code"] == 200:


            user_name = user_info["data"]["username"]
            name = user_info["data"]["full_name"]
            post = user_info["data"]["counts"]["media"]
            follows = user_info["data"]["counts"]["follows"]
            following = user_info["data"]["counts"]["followed_by"]

            print "\n\033[1;30;46m]", "Name = %s\nusername = %s\nTotal posts made = %d\nfollowing = %d\n%d people are following %s", %(name,user_name,post,follows,following,name.partition(" ")[0])

            print "\nEntering Main Menu...\n"
        else:
            print "Sorry! Your request cannot be served right now."

#===================================================GET_USER_ID METHOD=========================================================
#Method name: get_user_id(), to fetch user identification by passing instagram username
def get_user_id(insta_uname):

    #creating request url for accessing user information by giving username as the searching parameter

    request_url = (BASE_URL+ "users/search?q=%s&access_token=%s") %(insta_uname, ACCESS_TOKEN)
    print "GET request URL: %s\nLooking for user_id of: %s" %request_url,insta_uname


    #Making a request and saving the response in json format
    user_info = requests.get(request_url).json()

    #if request made is successful
    if user_info["meta"]["code"] == 200:

        #extracting the user_id and returning it in the form of json
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else:
            print "Ooops! Something went wrong"
    else:
        print "Oooops your request cannot be completed right now\nWe're very sorry\n"

    return None


#============================================================GET_USER_INFO METHOD====================================================

#method name: get_user_info(), used to fetch user details of an instagram user by passing instagram username

def get_user_info(insta_uname):

    #fetching user_id by calling get_user_id method
    user_id = get_user_id(insta_uname)

    if user_id == None:
        print "User does not exists"
        return  None
    #creating request url for accessing user information by giving user_id as parameter
    request_url = (BASE_URL+ "users/%s?access_token=%s") %(user_id, ACCESS_TOKEN)
    print "GET request url: %s\n" %request_url


    #Making the request and save the response in json format
    user_info = requests.get(request_url).json()

    #if request made is successfull
    if user_info["meta"]["code"] == 200:

        #Extracting details from the user_info in the json format
        if "data" in user_info:
            print "Username: %s\n" %insta_uname
            print "Number of followers: %d\n" %user_info["data"]["counts"]["followed_by"]
            print "Number of people you are following: %d\n" %user_info["data"]["counts"]["follows"]
            print "Number of posts: %d\n" %user_info["data"]["counts"]["media"]
        else:
            print "There is no data for this user"

    #if request made is unsucessfull
    else:
        print "Sorry your request cannot be processed right now\n"


#==================================================GET_OWN_POST METHOD===========================================================

#Method name: get_own_post(), used to fetch the recent post of the owner of access token

def get_own_post():

    #creating a request url for accessing recent post from own instagram account

    request_url = (BASE_URL+ "users/self/media/recent/?access_token=%s") %(ACCESS_TOKEN)
    print "GET request url: %s\n" %request_url

    #Making the request and save the response in jsnon format

    own_media = requests.get(request_url).json()

    #if request made is successfull
    if own_media["meta"]["code"] == 200:

        if len(own_media["data"]):
            #saving the image file in img_name variable and suffixing .jpeg extension
            img_name = own_media["data"][0]["id"] + ".jpeg"
            img_url = own_media["data"][0]["images"]["standard_resolution"]["url"]

            #downloading recent post as the img_name
            urllib.urlretrieve(img_url, img_name)

            #showing own recent post and returning media id

            print "Your image has been downloaded\nplease close your image viewer to proceed\n"
            os.system(img_name)
            return own_media["data"][0]["id"]
        #if there is no post to show
        else:
            print "There is no post to show\n"
            return "Sorry! No recent post to show."

    #if request made is unsuccessfull
    else:
        print "Oooops! Something went wrong\nYour request cannot be processed right now\n"
        return "Unsucessfull request!\n"

#====================================================GET_USER_POST METHOD===============================================
#Method name:get_user_post(), Used to fetch recent post of an instagram user by passiing the instagram username of the user

def get_user_post(insta_uname):
