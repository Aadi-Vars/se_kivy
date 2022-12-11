from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.popup import Popup
import requests
import time
Config.set('kivy', 'exit_on_escape', '0')

#changing background color
Window.clearcolor=(1,1,1,1)

sm=ScreenManager()

#__init__
seen_question=[]
selected_opt={}	


class paper_sub_scn(Screen):
	def back_to_home(self):
		
		global avai_exam,avai_paper,avai_language,undertaking_check,selected_opt,seen_question
		selected_question=[]
		avai_paper=[]
		avai_language={}
		selected_opt={}
		
		#restarting app
		app.root.clear_widgets()
		app.stop()
	
		app.run()
		sm.current="home"


class paper_scn(Screen):
	
	def submit(self):
		global sm,end_time
		end_time=time.time()
		
		spend_time=round((end_time-start_time)/60,3)
		popup=Popup(title="Completed!!",content=Label(text="You Spend "+str(spend_time)+" minutes"),size_hint=(0.8,0.2))
		popup.open()
		try:
			data=requests.get("https://raw.githubusercontent.com/Aadi-Vars/se.apk/Main/txt/se_submit.txt").text.split("\n")
			data.remove('')
		except:
			popup=Popup(title="Oops!!",content=(Label(text="Check Your Internet Connection")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return
			
		index=data.index(selected_exam+" "+selected_paper+" "+selected_language+" "+"Submit"+".kv")+1
		load_data=requests.get(data[index]).text
		Builder.load_string(load_data)
		
		global s
		s= paper_sub_scn(name='paper_sub_scn')
		sm.add_widget(s)
		sm.current="paper_sub_scn"
		
		global selected_opt
	
		for i in selected_opt:
			if type(selected_opt[i])==bool:
				s.ids[i].active=selected_opt[i]
				
			else:
				s.ids[i].text=selected_opt[i]
				
	
	def save_ans(self,btn):
		total_page=0
		for child in self.ids["pagelayout"].children:
			total_page+=1
			
		try:
			selected_opt[btn+"_opt1"]=self.ids[btn+"_opt1"].active
			selected_opt[btn+"_opt2"]=self.ids[btn+"_opt2"].active
			selected_opt[btn+"_opt3"]=self.ids[btn+"_opt3"].active
			selected_opt[btn+"_opt4"]=self.ids[btn+"_opt4"].active
			seen_question.append(btn)
		except:
			selected_opt[btn]=str(self.ids[btn].text)
			seen_question.append(btn)
		
		if self.ids["pagelayout"].page+1<total_page:
			self.ids["pagelayout"].page+=1




class main(App):
	def build(self):
		#home screen
		global home_scn
		home_scn=Screen(name="home")
		
		sm.add_widget(home_scn)

		global avai_exam,avai_paper,avai_language
		avai_exam=[]
		avai_paper=[]
		avai_language={}
		
		#trying to get data of exams
		try:
			data=requests.get("https://raw.githubusercontent.com/Aadi-Vars/se.apk/Main/txt/se.txt").text.split("\n")
			data.remove('')
		except:
			label=Label(text="Check Your Internet Connection",text_size=(Window.width,None),size_hint_x=None,width=Window.width,color=(0,0,0,1),halign="center")
			home_scn.add_widget(label)
			return sm
			
			#setting the details of exams and papers
		for i in data:
				if data.index(i)%2==0:
					i=i.rstrip(".kv")
					spt=i.split(" ")
					if i not in avai_exam:
						avai_exam.append(spt[0])
					avai_paper.append(spt[1])
					
					if spt[0]+spt[1] in avai_language:
						avai_language[spt[0]+spt[1]].append(spt[2])
					else:
						avai_language[spt[0]+spt[1]]=[spt[2]]
		
		
		home_main_box =BoxLayout(orientation="vertical")
		home_scn.add_widget(home_main_box)
		
		home_header_box =BoxLayout(orientation="vertical",size_hint_y=None,height=Window.height*0.1)
		home_main_box.add_widget(home_header_box)
		
		se_label=Label(text="S.E.\nSpecial Exam",color=(0,0,0),halign="center",font_size=60)
		home_header_box.add_widget(se_label)
		
		home_box =BoxLayout(orientation="vertical",padding=(Window.width*0.1,Window.height*0.35),spacing=Window.height*0.005,size_hint_y=None,height=Window.height*0.9)
		home_main_box.add_widget(home_box)
		
		global exam_drop,selected_exam
		exam_drop=DropDown()
		selected_exam=None
		

		# showing the avaiable exams
		for i in avai_exam:
			btn=Button(text=i,size_hint_y=None,height=Window.height*0.1)
			exam_drop.add_widget(btn)
			btn.bind(on_press=lambda btn: exam_drop.select(btn.text))
			btn.bind(on_release=self.paper)
		
		global paper_drop,selected_paper
		paper_drop=DropDown()
		selected_paper=None
		exam_btn=Button(text="Exam",on_release=exam_drop.open,background_color=(0,0,0,1),color=(1,1,1))
		home_box.add_widget(exam_btn)
		
		
		exam_drop.bind(on_select=lambda instance, x: setattr(exam_btn, 'text', x))
		
		paper_btn=Button(text="Paper",on_release=paper_drop.open,background_color=(0,0,0),color=(1,1,1))
		home_box.add_widget(paper_btn)
		
		paper_drop.bind(on_select=lambda instance, x: setattr(paper_btn, 'text', x))
		
		submit_btn=Button(text="Next",on_release=self.instr_scn_build,background_color=(0,0,0),color=(1,1,1))
		
		home_box.add_widget(submit_btn)
		

		return sm
		
	def selected_paper_func(self,btn):
		#setting selected paper
		global selected_paper,avai_paper
		selected_paper=btn.text
		
	def paper(self,btn):
		#setting the available paper
		global paper_drop,avai_paper,selected_exam
		
		selected_exam=btn.text
				
		for i in avai_paper:
			btn=Button(text=i,size_hint_y=None,height=Window.height*0.1)
			paper_drop.add_widget(btn)
			btn.bind(on_release=lambda btn: paper_drop.select(btn.text))
			btn.bind(on_press=self.selected_paper_func)
			
	
	
	
	def back_to_home(self,btn):
		global sm
		sm.current="home"
		sm.transition.direction="right"
		
	def instr_scn_build(self,btn):
		global sm
		# instruction screen
		if selected_exam==None:
			popup=Popup(title="Oops!!",content=(Label(text="You have not selected any Exam")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return 
		
		if selected_paper==None:
			popup=Popup(title="Oops!!",content=(Label(text="You have not selected any Paper")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return 
		
		global instr_scn
		instr_scn=Screen(name="instr")
		sm.add_widget(instr_scn)
		sm.current="instr"
		sm.transition.direction="left"
		
		instr_main_box= BoxLayout(orientation="vertical")
		instr_scn.add_widget(instr_main_box)
		
		instr_header_box= BoxLayout(orientation="vertical",size_hint_y=None,height=Window.height*0.1)
		instr_main_box.add_widget(instr_header_box)
		
		instr_label=Label(text="Instructions",color=(0,0,0),halign="center",font_size=60)
		instr_header_box.add_widget(instr_label)
		
		instr_scroll=ScrollView()
		instr_main_box.add_widget(instr_scroll)
		
		instr_box= BoxLayout(orientation="vertical",size_hint_y=None,height=Window.height*0.95,padding=(Window.width*0.01,0))
		instr_scroll.add_widget(instr_box)
		
		label=Label(text="Please read the instruction carefully",text_size=(Window.width*0.9,None),size_hint=(None,None),width=Window.width*0.95,bold=True,color=(0,0,0,1),height=Window.height*0.05)
		instr_box.add_widget(label)
		
		instr_label=Label(text="1. Total duration of examinatiom is enough to complete the paper\n2. The clock will be set at server. The time consumed will be displayed after the submission of paper\n3. To nagivate through the question do the following:\n    a. Swipe left to right to go to the previous question\n    b. Swipe right to left to go to the next question\n    c. Click on Save button to save your answer and go to the next question\n4. Procedure for answering a multiple choice type question:\n    a.To select answer click on the button of one of the option\n    b. To deselect your chosen answer click on the Clear Response button\n    c. To change your option click on the button of another option\n    d. To save you answer you MUST click on Save Button\n    e.To change your answer of a question that have already being answered,first navigate to that question for answering,then follow the procedure to answer that type of question\n5. After clicking on the Save button on the last question of a section,you will be automatically bring to the first question of next section\n6. You can shuffle between the question and the section anytime during the examination according to your convenience",text_size=(Window.width*0.9,None),size_hint=(None,None),width=Window.width*0.95,color=(0,0,0,1),height=Window.height*0.85)
		
		instr_box.add_widget(instr_label)
		
		instr_box2 =BoxLayout(orientation="horizontal",size_hint_y=None,height=Window.height*0.1,spacing=Window.width*0.01)
		instr_main_box.add_widget(instr_box2)
		
		
		prev_btn=Button(text="Previous",color=(1,1,1),size_hint=(None,None),width=Window.width*0.5,height=Window.height*0.05,on_release=self.back_to_home)
		
		instr_box2.add_widget(prev_btn)
	
		next_btn=Button(text="Next",background_color=(0,0,0),color=(1,1,1),size_hint=(None,None),width=Window.width*0.5,height=Window.height*0.05,on_release=self.other_instr_build)
		
		instr_box2.add_widget(next_btn)
	
	def back_to_instr(self,btn):
		global sm
		sm.current="instr"
		sm.transition.direction="right"
		
	def other_instr_build(self,btn):
		global sm,other_instr_scn
		#other instruction screen
		other_instr_scn=Screen(name="other instr")
		sm.add_widget(other_instr_scn)
		sm.current="other instr"
		sm.transition.direction="left"
		other_instr_main_box=BoxLayout(orientation="vertical")
		other_instr_scn.add_widget(other_instr_main_box)
		
		other_instr_header_box= BoxLayout(orientation="vertical",size_hint_y=None,height=Window.height*0.1)	
		other_instr_main_box.add_widget(other_instr_header_box)
		
		other_instr_label=Label(text="Other Important Instruction",color=(0,0,0),bold=True)
		other_instr_header_box.add_widget(other_instr_label)
		
		scroll=ScrollView()
		other_instr_main_box.add_widget(scroll)
		
		other_instr_box= BoxLayout(orientation="vertical",size_hint_y=None,height=Window.height*0.4)
		scroll.add_widget(other_instr_box)
		
		box= BoxLayout(orientation="horizontal",size_hint_y=None,height=Window.height*0.05)
		other_instr_box.add_widget(box)
		
		label=Label(text="Choose your language: ",size_hint_x=None,width=Window.width*0.6,text_size=(Window.width*0.6,None),color=(0,0,0,1))
		box.add_widget(label)
		global selected_language
		selected_language=None
		language_drop=DropDown()
		for i in avai_language[selected_exam+selected_paper]:
			btn=Button(text=i,size_hint=(None,None),width=Window.width*0.2)
			language_drop.add_widget(btn)
			btn.bind(on_press=lambda btn :language_drop.select(btn.text))
			btn.bind(on_release=self.select_language)
		
		main_button =Button(text="Language",on_release=language_drop.open,size_hint_x=None,width=Window.width*0.2)
		box.add_widget(main_button)
		language_drop.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
		
		box2= BoxLayout(orientation="horizontal")
		other_instr_box.add_widget(box2)
	
		global undertaking_check
		undertaking_check= CheckBox(size_hint_x=None,width=Window.width*0.1,color=(0,0,0,1))
		box2.add_widget(undertaking_check)
		
		label=Label(text="I have read and understood the instruction carefully and I will be fully reponsible of any mistake made by me",color=(0,0,0,1),text_size=(Window.width*0.8,None),size_hint_x=None,width=Window.width*0.8)
		box2.add_widget(label)
		
			
		other_instr_box2 =BoxLayout(orientation="horizontal",size_hint_y=None,height=Window.height*0.1,spacing=Window.height*0.001)
		other_instr_main_box.add_widget(other_instr_box2)
		
		prev_btn=Button(text="Previous",color=(1,1,1),size_hint=(None,None),width=Window.width*0.5,height=Window.height*0.05,on_release=self.back_to_instr)
		
		other_instr_box2.add_widget(prev_btn)
	
		next_btn=Button(text="Next",background_color=(0,0,0),color=(1,1,1),size_hint=(None,None),width=Window.width*0.5,height=Window.height*0.05,on_release=self.paper_scn_build)
		
		other_instr_box2.add_widget(next_btn)
		
	def select_language(self,btn):
		#setting selected language
		global selected_language
		selected_language=str(btn.text)
		
	def paper_scn_build(self,btn):
		global sm,undertaking_check,start_time
		start_time=time.time()
		
		if undertaking_check.active==False:
			popup=Popup(title="Oops!!",content=(Label(text="You have not check the undertaking")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return
		
		if selected_language==None:
			popup=Popup(title="Oops!!",content=(Label(text="You have not select any language")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return
		
		#trying to fetch questions
		try:
			data=requests.get("https://raw.githubusercontent.com/Aadi-Vars/se.apk/Main/txt/se.txt").text.split("\n")
			data.remove('')
		except:
			popup=Popup(title="Oops!!",content=(Label(text="Check Your Internet Connection")),size_hint=(None,None,),size=(Window.width*0.7,Window.height*0.2))
			popup.open()
			return
			
		index=data.index(selected_exam+" "+selected_paper+" "+selected_language+".kv")+1
		
		load_data=requests.get(data[index]).text
		#loading the kv file of question
		Builder.load_string(load_data)
	
		sm.add_widget(paper_scn(name="paper_scn"))
		sm.current="paper_scn"
		sm.transition.direction="left"
		
	
		
		
app=main()
app.run()
		