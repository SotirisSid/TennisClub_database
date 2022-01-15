
from itertools import combinations
import itertools
import sqlite3 as lite
from unittest import result

from numpy import select
from pandas.core import series
from prettytable import PrettyTable
import pandas as pd
import datetime
from dateutil.relativedelta import *
import random
## Γινεται το αρχικο connection στην βαση
def connect_to_db(db_name):
    global c,con
    try:
        con = lite.connect(db_name+'.db')
        c= con.cursor()
        print("connected to database")
    except:
        print("something went wrong")
        exit()
    
def strtodate(string): #Μετατρέπει ένα str σε datetime ώστε να το στέλνουμε στη βάση
    #string format day - month - year
    string = string.split('-')
    year = int(string[0])
    month = int(string[1])
    day = int(string[2])
    return datetime.date(year,month,day)
    
def valid_date(str_in): #Έλεγχος για την εγκυρότητα μιας ημερομηνίας που έχει εισηχθεί σε μορφή DD-MM-YYYY
    try:
        newDate = datetime.datetime(day=int(str_in[0:2]),month=int(str_in[3:5]),year=int(str_in[6:10]))
        return True
    except ValueError:
        return False
def get_win(id):
    c.execute("Select wins from ΑΘΛΗΤΗΣ where id_member='"+str(id)+"'")
    result=c.fetchone()
    return result[0]
def add_courts():
    loc=input("location:")
    ter=input("terrain:")
    price=input("price:")
    c.execute("select * from ΓΗΠΕΔΟ")
    i=len(c.fetchall())
    c.execute("INSERT INTO ΓΗΠΕΔΟ (id_court,location,terrain,number_of) VALUES(?,?,?,?)",(i,loc,ter,price))
    print("element added to db")
    con.commit()

def find_tournament_id():
    c.execute("SELECT max(id_tournament) from ΤΟΥΡΝΟΥΑ")
    result=c.fetchone()
    id_tour=int(result[0])+1
    return id_tour


def atomo_id(f_name,l_name,phone_num):
    c.execute("SELECT * from ΑΘΛΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
    result=c.fetchone()
    return result[0]
def atomo_level(f_name,l_name,phone_num):
    c.execute("SELECT * from ΑΘΛΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
    result=c.fetchone()
    return result[6]

## functions for checking if a memeber or teacher exists in the database if the person exists it returns 1 else 0
def check_member(f_name,l_name,phone_num):
    ##query=("SELECT * from ΑΘΛΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
    c.execute("SELECT * from ΑΘΛΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
    if(c.fetchone()):
        return 1
    else:
        return 0
## funciont to check if member is subscriber
def check_subscription(f_name,l_name,phone_num):
    check1=check_member(f_name,l_name,phone_num)
    if(check1==1):
        c.execute("SELECT * from ΑΘΛΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
        result=c.fetchone()
        print(result[0])
        c.execute("SELECT id_member from ΣΥΝΔΡΟΜΗΤΗΣ WHERE id_member=?",(str(result[0])))
        ##c.execute("SELECT * from ΣΥΝΔΡΟΜΗΤΗΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
        if(c.fetchone()):
            print("exists")
            return 1
        else:
            print("doesnt exist")
            return 0
    else:
        return 0

def check_instr(f_name,l_name,phone_num):
    c.execute("SELECT * from ΔΑΣΚΑΛΟΣ WHERE first_name=? AND last_name=? AND phone_number=?",(f_name,l_name,phone_num))
    if(c.fetchone()):
        return 1
    else:
        return 0

def subscription(id):
    print("Θα ήθελες να γίνεις συνδρομητής στο club? (0,1)")
    ans=input()
    if(ans=="0"):
        print("continuing as guest...")
        
        c.execute("INSERT INTO ΕΝΟΙΚΙΑΣΤΗΣ (id_member) VALUES(?) ",str(id))
        con.commit()
    elif(ans=="1"):
        print("select packet (1=1 month for 35$,2=6 months for 150$,3=1year for 290$")
        ans2=input()
        if(ans2=="1"):
            amount=35
            kind="1 month"
            startdate=datetime.datetime.now().date()
            enddate=startdate+ relativedelta(months=1)
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗ (start_date,end_date,amount,kind_of,id_sub)  VALUES(?,?,?,?,?)",(startdate,enddate,amount,kind,id))
            con.commit()
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗΤΗΣ (id_member,payment)  VALUES(?,?)",(id,True))
            con.commit()
        elif(ans2=="2"):
            amount=150
            kind="6 month"
            startdate=datetime.datetime.now().date()
            enddate=startdate+ relativedelta(months=6)
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗ (start_date,end_date,amount,kind_of,id_sub)  VALUES(?,?,?,?,?)",(startdate,enddate,amount,kind,id))
            con.commit()
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗΤΗΣ (id,payment)  VALUES(?,?)",(id,True))
            con.commit()
        elif(ans2=="3"):
            amount=290
            kind="12 month"
            startdate=datetime.datetime.now().date()
            enddate=startdate+ relativedelta(months=12)
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗ (start_date,end_date,amount,kind_of,id_sub)  VALUES(?,?,?,?,?)",(startdate,enddate,amount,kind,id))
            con.commit()
            c.execute("INSERT INTO ΣΥΝΔΡΟΜΗΤΗΣ (id,payment)  VALUES(?,?)",(id,True))
            con.commit()
        else: 
            print("Μη έγκυρη επιλογή")
    else: 
        print("Μη έγκυρη επιλογή")
            



## registers a member to the database
def register_member():

    while(True):
        try:

            fname=input("Να γινει εισαγωγή του ονόματος\n")
            lname=input("Να γινει εισαγωγή του επωνύμου\n")
            address=input("Να γίνει εισαγωγή της Διεύθυνσης\n")
            phone_number=input("Να γίνει εισαγωγή του τηλεφώνου\n")
            level=input("Να γίνει εισαγωγή του επιπέδου του παίκτη\n")
            medical=input("Να γίνει εισαγωγή της βεβαίωσης ιατρού\n")
            check=check_member(fname,lname,phone_number)
            if(check==0):
                c.execute("Select * from ΑΘΛΗΤΗΣ")
                id=len(c.fetchall())
                c.execute("INSERT INTO ΑΘΛΗΤΗΣ (id_member,first_name,last_name,address,phone_number,medical_att,level) VALUES(?,?,?,?,?,?,?)",(id,fname,lname,address,phone_number,medical,level))
                con.commit()
                print("Η εγγραφη ολοκληρώθηκε")
                subscription(id)
                more=input("Επιθυμείτε να προσθέσετε και άλλο άτομο?(0,1)\n")
                if(more=="0"):
                    return
            else:
                print("Υπαρχει ήδη αυτό το όνομα\n")
        
        except:

            print("Αδυναμία εισαγωγής ατόμου")
            return
#registers an instructor to the database
def register_instructor():
    while(True):
        try:
            fname=input("Να γινει εισαγωγή του ονόματος\n")
            lname=input("Να γινει εισαγωγή του επωνύμου\n")
            address=input("Να γίνει εισαγωγή της Διεύθυνσης\n")
            phone_number=input("Να γίνει εισαγωγή του τηλεφώνου\n")
            address=input("Να γίνει εισαγωγή της Διεύθυνσης")
            check=check_member(fname,lname,phone_number)
            if(check==0):
                c.execute("Select * from ΔΑΣΚΑΛΟΣ")
                id=len(c.fetchall())
                c.execute("INSERT INTO ΔΑΣΚΑΛΟΣ (id_teacher,first_name,last_name,phone_number,address) VALUES(?,?,?,?,?)",(id,fname,lname,phone_number,address))
                con.commit()
                print("Η εγγραφη ολοκληρώθηκε")
                more=input("Επιθυμείτε να προσθέσετε και άλλο άτομο?(0,1)\n")
                if(more=="0"):
                    return
            else:
                print("Υπαρχει ήδη αυτό το όνομα\n")
        except:
            print("Αδυναμία ολοκλήρωσης εγγραφής")
            return


def search_in_db(table):
    
    query = ("SELECT id_court FROM ")+table
    c.execute(query)

    df = pd.read_sql(query, con)
    con.close()
    print(df)
    for x in df:
        print(x)

def view_available_courts(date,time):
    query="SELECT *FROM ΓΗΠΕΔΟ WHERE id_court is not ( select id_court from ΚΡΑΤΗΣΗ_ΓΗΠΕΔΟΥ where date="+date+" or time="+time+"  )"
    c.execute(query)
    df = pd.read_sql(query, con)
    print("Διαθέσιμα γήπεδα")
    return df

##########################################################
def krathsh(mode):
    if(mode==0):
        print("Δώστε το ονομα σας")
        ans1=input()
        print("Δώστε το επώνυμο σας")
        ans2=input()
        print("Δώστε τον αριθμο τηλεφώνου")
        phone=input()
        try:
            id=atomo_id(ans1,ans2,phone)
        except:
            print("Πρεπει να ειστε μέλος για να κάνετε κράτηση")
            menu()
        date=input("Να γίνει εισαγωγή της ημερομηνίας που θελετε να γινει η κράτηση\n")
        time=input("Να γίνει εισαγωγή της ώρας που θέλετε να γίνει η κράτηση\n")  
        if(valid_date(date)):
            print(view_available_courts(date,time))
            while(1):
                selection=input("Διαλέξτε διαθέσιμο γήπεδο για κράτηση")
                print(selection,id,date,time)
                c.execute("INSERT INTO ΚΡΑΤΗΣΗ_ΓΗΠΕΔΟΥ (id_reservation,id_court,id_member,date,time,id_tournament) VALUES(?,?,?,?,?,?)",(None,selection,id,date,time,None))
                con.commit()
        else:
            print("Υπήρξε πρόβλημα με την κράτηση")


    if(mode==1):
        date=input("Να γίνει εισαγωγή της ημερομηνίας που θελετε να γινει το τουρνουά\n")
        time=input("Να γίνει εισαγωγή της ώρας που θέλετε να γίνει το τουρνουά\n") 
        level=input("Επέλεξε επίπεδο (Αρχάριος ή Προχωρημένος\n")
        if(valid_date(date)):
            print(view_available_courts(date,time))
            while(1):
                selection=input("Διαλέξτε διαθέσιμο γήπεδο για κράτηση")
                print(selection,id,date,time)
                tour_id=find_tournament_id()
                c.execute("INSERT INTO ΚΡΑΤΗΣΗ_ΓΗΠΕΔΟΥ (id_reservation,id_court,id_member,date,time,id_tournament) VALUES(?,?,?,?,?,?)",(None,selection,None,date,time,tour_id))
                con.commit()
                
                c.execute("INSERT INTO ΤΟΥΡΝΟΥΑ (id_reservation,level) VALUES(?,?)",(tour_id,level))
                con.commit()
        
## δείχνει τα διαθέσιμα για εγγραφη τουρνουά 
def view_available_tournaments(level):
    query="SELECT * from ΤΟΥΡΝΟΥΑ,ΚΡΑΤΗΣΗ_ΓΗΠΕΔΟΥ where level='"+level+"' AND ΤΟΥΡΝΟΥΑ.id_tournament=ΚΡΑΤΗΣΗ_ΓΗΠΕΔΟΥ.id_tournament and date>strftime('%d-%m-%Y','now')"
    c.execute(query)
    df = pd.read_sql(query, con)
    print("Διαθέσιμα Τουρνουά")
    print(df)

## επιτρεπει σε ενα ατομο να κανει εγγραφη σε ενα τουρνουα 
def register_to_tournament(mode):
    print("Δώστε το ονομα σας")
    ans1=input()
    print("Δώστε το επώνυμο σας")
    ans2=input()
    print("Δώστε τον αριθμο τηλεφώνου")
    phone=input()
    id=atomo_id(ans1,ans2,phone)
    wins=0
    if(mode==0):
        tour_level="Αρχάριος"
        person_level=atomo_level(ans1,ans2,phone)
        if(tour_level==person_level):
            view_available_tournaments()
            tour_id=input("δίαλεξε το id του τουρνουά που θελεις να συμμετασχεις")
            query="UPDATE ΑΘΛΗΤΗΣ SET id_tournament='"+tour_id+"' , wins='"+str(wins)+"' where id_member='"+str(id)+"'"
            c.execute(query)
            con.commit()
            
        else:
            print("Το επίπεδο σας ειναι μεγαλύτερο απο το επιτρεπτό")

    if(mode==1):

        level=" "
        person_level=atomo_level(ans1,ans2,phone)
        if(level==person_level):
           
            query="UPDATE ΑΘΛΗΤΗΣ SET id_tournament='"+tour_id+"' , wins='"+str(wins)+"' where id_member='"+str(id)+"'"
            con.commit()
            
        else:
            print("Το επίπεδο σας ειναι μικροτερο απο το επιτρεπτό")
        

## to ftiaxnw aurio

def kratisi_menu(): #Σε αυτό το μενού σχεδιάζονται οι επιλογές της κράτησης
    while True:
        print("Κρατήσεις")
        t = PrettyTable(['Επιλογή','Περιγραφή',]) 
        t.add_row([1,"Νέα Κράτηση"])
        t.add_row([2,"Αλλαγή σε Κράτηση"])
        t.add_row(["Κενό","Έξοδος"])
        print(t)
        print("Ανάλογα με το ποια λειτουργία θέλετε επιλέξτε το αντίστοιχο νούμερο")
        print("Αν θέλετε να κλείσετε την εφαρμογή πατήστε το κενό")
        ans =input("Επιλογή: ")
                   
        if ans=='1':
            print("")
            ## synarthsh poy kanei krathsh
        if ans=='2':
            print("")
            ## sunarthsh poy allazei uparxousa krathsh
        if ans==' ':
            return


## selects an instructor for tutoring
def select_instructor():
    query="SELECT * from ΔΑΣΚΑΛΟΣ"
    print("Δώστε το ονομα σας")
    ans1=input()
    print("Δώστε το επώνυμο σας")
    ans2=input()
    print("Δώστε τον αριθμο τηλεφώνου")
    phone=input()
    check=check_subscription(ans1,ans2,phone)  ## checks if the member is subscribed .if it is he can select instructor
    if(check==1):
        while(1):
            
                print("Διαλέξτε έναν απο τους υπάρχοντες δασκάλους")
                c.execute("Select * from ΔΑΣΚΑΛΟΣ")
                df = pd.read_sql("Select * from ΔΑΣΚΑΛΟΣ", con)
                num_of_rows=len(c.fetchall())
                print(num_of_rows)
                print(df)
                at_id=atomo_id(ans1,ans2,phone)
                teacher_id=input()
                if(int(teacher_id)<num_of_rows and int(teacher_id)>=0):
                    c.execute("INSERT INTO ΔΙΔΑΣΚΑΛΙΑ (id_teacher,id_sub) VALUES (?,?)",(teacher_id,at_id))
                    con.commit()
                    print("Έγινε η επιλογή δασκάλου")
                    menu()
                else:
                    print("Λάθος επιλογή")
    else:
        print("Δεν δικαιούστε δάσκαλο.Για να αποκτήσετε αυτήν την δυνατότητα πρέπει να γίνεται συνδρομητής")
        menu()




## view all the courts (not the available ones for a specific time)
def view_courts():
    print("Αυτά είναι όλα τα γήπεδα μας")
    c.execute("SELECT * FROM ΓΗΠΕΔΟ")
    result=c.fetchall()

    for i in result:
        print(i)
    print("Θα θέλατε να κάνετε μια κράτηση?")
    ans=input("(0,1)")
    if(ans==1):
        krathsh(0)
    else:
        menu()
##view all athletes in the database
def view_atoma():
    print("Αυτά είναι όλα τα Μέλη μας")
    c.execute("SELECT * FROM ΑΘΛΗΤΗΣ")
    result=c.fetchall()

    for i in result:
        print(i)


def menu(): #Σε αυτό το μενού πρέπει να σχεδιάσουμε τις επιλογές
    print('Καλησπέρα!\n')
    while True:
        print("Κεντρικό Μενού")
        t = PrettyTable(['Επιλογή','Περιγραφή',]) 
        t.add_row([1,"Κρατήσεις"])
        t.add_row([2,"Άτομα"])
        t.add_row([3,"Τουρνουά"])
        t.add_row([4,"Γκρουπ Διδασκαλίας"])
        t.add_row([5,"Γήπεδα"])
        t.add_row(["Κενό","Έξοδος"])
        print(t)
        print("Ανάλογα με το ποια λειτουργία θέλετε επιλέξτε το αντίστοιχο νούμερο")
        print("Αν θέλετε να κλείσετε την εφαρμογή πατήστε το κενό ")
        ans =input("Επιλογή: ")
        if(ans=="1"):
            krathsh(0)
        if (ans=="2"):
            ans2=input("Θέλετε να γίνει εγγραφή ατόμου η δασκάλου (Δυνατές επιλογές 1 ή 2)")
            if(ans2=="1"):
                register_member()
            elif (ans2=="2"):
                register_instructor()
            else:
                print("Μη έγκυρη επιλογή Δυνατές επιλογές 1 ή 2)")
        if(ans=="3"):
            krathsh(1)
        if(ans=="4"):
            select_instructor()
        if(ans=="5"):
            view_courts()

        if(ans==" "):
            return





## διαλεγει εναν τυχαιο αντιπαλο με ιδιο επιπεδο 
def select_random_opponent():
    print("Δώστε το ονομα σας")
    ans1=input()
    print("Δώστε το επώνυμο σας")
    ans2=input()
    print("Δώστε το επίπεδο σας (Αρχάριος, Προχωρημένος)")
    level=input()
    print("Δώστε τον αριθμο τηλεφώνου")
    phone=input()

    check=check_member(ans1,ans2,phone)
    if(check==1):

    
        query="SELECT id_member From ΑΘΛΗΤΗΣ WHERE level='"+level+"' and first_name!='"+ans1+"' and last_name!='"+ans2+"'"
        c.execute(query)
        num_of_rows=len(c.fetchall())-1
        df = pd.read_sql(query, con)
        con.close()
        num=random.randint(0,num_of_rows)
        return df.loc[num]["id_member"]
    else:
        print("Δεν υπάρχει αυτό το άτομο στην βάση")

  ##  con.commit

def random_matches(tour_id):
    query="select * from ΑΘΛΗΤΗΣ where id_tournament=' "+str(tour_id)+"'"
    c.execute(query)
    result=c.fetchall()
    max=len(result)
    match_score=[]
    ids=[]
    counter=0
    for i in range(0,int(max)):
        ids.append(result[i][0])
    matches=list(itertools.combinations(ids,2))
    for i in matches:
        counter=counter+1
        score=(random.randint(0,3),random.randint(0,3))
        match_score.append(score)
    print(match_score)
    print(matches)
    
    ## add id match score and matches to database
    
    for i in range(0,counter):
        score=str(match_score[i][0])+"-"+str(match_score[i][1])
        query="INSERT INTO ΑΓΩΝΑΣ (id_player_1,id_player_2,id_game,score,id_court,id_tournament) VALUES(?,?,?,?,?,?)"
        c.execute(query,(str(matches[i][0]),(matches[i][1]),None,score,str(2),tour_id))
        con.commit()
        if(int(match_score[i][0])>int(match_score[i][1])):
            wins=int(get_win(matches[i][0]))
            wins=wins+1
            c.execute("UPDATE ΑΘΛΗΤΗΣ SET wins='"+str(wins)+"' where id_member='"+str(matches[i][0])+"'")
        if(int(match_score[i][0])<int(match_score[i][1])):
            wins=int(get_win(matches[i][1]))
            wins=wins+1
            c.execute("UPDATE ΑΘΛΗΤΗΣ SET wins='"+str(wins)+"' where id_member='"+str(matches[i][1])+"'")
        



   
    
    






def test():
    tour_id="2"
    wins="0"
    id=0
    query="UPDATE ΑΘΛΗΤΗΣ SET id_tournament='"+tour_id+"' , wins='"+wins+"' where id_member='"+str(id)+"'"
    c.execute(query)
    con.commit()


if __name__=="__main__":
   connect_to_db("tennis_club")
  ## random_matches(2)
   menu()
  
   ##find_tournament_id()
   ##krathsh(0)
   ##check_subscription("Ορέστης","Ζερβός","1223456789")
   ##select_instructor()
  ##print(atomo_id("Ορέστης","Ζερβός","1223456789"))
   ##elect_random_opponent()
 ## search_in_db("ΓΗΠΕΔΟ")
   ##add_courts(c,con) 
  ## search_in_db("ΓΗΠΕΔΟ")
   ##menu()
   ##Σωτηρης	Σιδηρόπουλος	Αδειμάντου	6978986722