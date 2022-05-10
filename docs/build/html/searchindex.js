Search.setIndex({docnames:["flask_app","flask_app.backend","index","modules","run","tests"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["flask_app.rst","flask_app.backend.rst","index.rst","modules.rst","run.rst","tests.rst"],objects:{"":{run:[4,0,0,"-"]},"flask_app.app":{create_app:[0,1,1,""]},"flask_app.backend":{courses:[1,0,0,"-"],schedule:[1,0,0,"-"]},"flask_app.backend.courses":{APIGet:[1,2,1,""],APIParse:[1,2,1,""],Course:[1,2,1,""],CourseList:[1,2,1,""],MeetingTime:[1,2,1,""],Professor:[1,2,1,""],RequestProxy:[1,2,1,""],Section:[1,2,1,""]},"flask_app.backend.courses.APIGet":{get_complete_course_by_course_code:[1,3,1,""],get_course_head_by_course_code:[1,3,1,""],get_course_heads_by_query:[1,3,1,""],get_course_list_by_gen_ed:[1,3,1,""],get_course_list_by_page_number:[1,3,1,""],get_professor_by_name:[1,3,1,""],get_professor_gpa_breakdown_by_course:[1,3,1,""],get_sections_list_by_course:[1,3,1,""],headers:[1,4,1,""]},"flask_app.backend.courses.APIParse":{planetterp_course_raw_to_course_head:[1,3,1,""],planetterp_prof_raw_to_prof_head:[1,3,1,""],planetterp_raw_grade_distribution_to_gpa:[1,3,1,""],umd_io_course_raw_to_course_head:[1,3,1,""],umd_io_sections_raw_to_section_list:[1,3,1,""]},"flask_app.backend.courses.Course":{get_professor_average_rating:[1,3,1,""],set_sorted_professors_by_rating:[1,3,1,""],toJSON:[1,3,1,""]},"flask_app.backend.courses.CourseList":{get_course_using_course_code:[1,3,1,""],get_courses_using_page_number:[1,3,1,""],make_meeting_dict:[1,3,1,""]},"flask_app.backend.courses.Professor":{get_all_professors:[1,3,1,""]},"flask_app.backend.courses.RequestProxy":{bad_request:[1,4,1,""],planetterp_get_course_by_course_code:[1,3,1,""],planetterp_get_courses_by_page:[1,3,1,""],planetterp_get_grades_by_course_code:[1,3,1,""],planetterp_get_professor_by_name:[1,3,1,""],planetterp_search_by_query:[1,3,1,""],test_mode:[1,4,1,""],umdio_get_courses_by_gened:[1,3,1,""],umdio_get_sections_by_course_code:[1,3,1,""]},"flask_app.backend.courses.Section":{get_formatted_weekly_schedule:[1,3,1,""]},"flask_app.backend.schedule":{MySchedule:[1,2,1,""]},"flask_app.backend.schedule.MySchedule":{ScheduleWarning:[1,2,1,""],add_course:[1,3,1,""],add_registered_course_section_by_id:[1,3,1,""],add_section:[1,3,1,""],check_section_no_time_conflicts:[1,3,1,""],colors:[1,4,1,""],get_course_color:[1,3,1,""],get_schedule_average_gpa:[1,3,1,""],get_serialized_schedule:[1,3,1,""],load_serialized_schedule:[1,3,1,""],remove_all_classes:[1,3,1,""],remove_course:[1,3,1,""],remove_registered_course_section_by_id:[1,3,1,""],remove_section:[1,3,1,""]},"flask_app.forms":{AddClassForm:[0,2,1,""],AddRemoveForm:[0,2,1,""],AddSectionForm:[0,2,1,""],ClearAllCoursesForm:[0,2,1,""],GenEdSearchForm:[0,2,1,""],NextPageOnAllCoursesPageForm:[0,2,1,""],PreviousPageOnAllCoursesPageForm:[0,2,1,""],SearchForCourseForm:[0,2,1,""],SearchForm:[0,2,1,""],SerializeScheduleForm:[0,2,1,""],ViewSectionsForm:[0,2,1,""]},"tests.conftest":{app:[5,1,1,""],client:[5,1,1,""]},"tests.test_app":{test_all_courses_returns_200:[5,1,1,""],test_all_professors_returns_200:[5,1,1,""],test_index_returns_200:[5,1,1,""],test_professor_detail_returns_200:[5,1,1,""],test_professor_detail_returns_404_if_no_professor:[5,1,1,""],test_tutorial_returns_200:[5,1,1,""]},"tests.test_courses":{APIGetAndParseTest:[5,2,1,""],CourseListTest:[5,2,1,""],CourseTest:[5,2,1,""]},"tests.test_courses.APIGetAndParseTest":{setUp:[5,3,1,""],tearDown:[5,3,1,""],test_gen_ed_search_returned_courses_empty_bad_request:[5,3,1,""],test_gen_ed_search_returned_courses_valid_good_request:[5,3,1,""],test_get_course_heads_make_sure_all_courses_we_expect_are_present:[5,3,1,""],test_professor_object_returned_valid_courselist:[5,3,1,""],test_professor_object_returned_valid_instructor_type:[5,3,1,""],test_professor_object_returned_valid_name:[5,3,1,""],test_professor_object_returned_valid_rating:[5,3,1,""]},"tests.test_courses.CourseListTest":{setUp:[5,3,1,""],tearDown:[5,3,1,""],test_get_courses_using_course_code_invalid_course_code_throws_exception:[5,3,1,""],test_get_courses_using_course_code_valid_course_code:[5,3,1,""],test_get_courses_using_invalid_page_number:[5,3,1,""],test_get_courses_using_valid_page_number:[5,3,1,""]},"tests.test_courses.CourseTest":{test_class_formatted_weekly_schedule_correct:[5,3,1,""],test_course_correct_prof_rating_order:[5,3,1,""],test_course_correct_professor_rating_static_method:[5,3,1,""],test_course_empty_prof_rating_order:[5,3,1,""],test_hashes_of_different_meetings_times_are_different_too:[5,3,1,""],test_hashes_of_same_meetings_times_are_same:[5,3,1,""],test_meeting_time_not_equal_to_non_meeting_time_object:[5,3,1,""],test_meeting_times_are_equal_according_to_eq_function:[5,3,1,""],test_meeting_times_are_not_equal_according_to_eq_function:[5,3,1,""]},"tests.test_schedule":{ScheduleGPA:[5,2,1,""],ScheduleTest:[5,2,1,""],ScheduleWarningTest:[5,2,1,""]},"tests.test_schedule.ScheduleGPA":{test_correct_average_gpa:[5,3,1,""],test_empty_schedule_zero_gpa:[5,3,1,""]},"tests.test_schedule.ScheduleTest":{test_add_class_and_credits_and_schedule_correct:[5,3,1,""],test_add_class_then_remove_class_correct_credits_and_schedule:[5,3,1,""],test_add_duplicate_class_and_credits_and_schedule_correct:[5,3,1,""],test_add_duplicate_course_doesnt_add_again:[5,3,1,""],test_add_two_classes_correct_credits_and_schedule:[5,3,1,""],test_add_two_classes_make_sure_ordered_by_time:[5,3,1,""],test_class_formatted_weekly_schedule_correct:[5,3,1,""],test_class_overlap_different_class_time_conflict:[5,3,1,""],test_class_overlap_same_class:[5,3,1,""],test_class_with_no_time_conflict:[5,3,1,""],test_get_course_color_of_course_in_schedule:[5,3,1,""],test_get_course_color_of_course_not_in_schedule:[5,3,1,""],test_load_empty_serialized_schedule:[5,3,1,""],test_load_serialize_schedule_works:[5,3,1,""],test_load_serialized_schedule_invalid_course:[5,3,1,""],test_load_serialized_schedule_invalid_course_format:[5,3,1,""],test_load_serialized_schedule_invalid_section_for_valid_course:[5,3,1,""],test_remove_all_classes_on_empty_schedule:[5,3,1,""],test_remove_all_classes_on_schedule_with_classes_in_it:[5,3,1,""],test_remove_course_actually_in_schedule:[5,3,1,""],test_remove_course_not_in_schedule:[5,3,1,""],test_removing_class_not_in_schedule_doesnt_change_credits:[5,3,1,""],test_schedule_is_empty:[5,3,1,""],test_serialize_empty_schedule:[5,3,1,""],test_serialize_schedule_returns_comma_separated_section_ids:[5,3,1,""],test_try_to_add_class_in_middle_of_day_start_time_overlaps_with_previous_end_time:[5,3,1,""],test_try_to_add_overlapping_classes_only_first_gets_added:[5,3,1,""]},"tests.test_schedule.ScheduleWarningTest":{test_add_class_no_open_seats_makes_warning:[5,3,1,""],test_add_multiple_classes_no_open_seats_makes_warnings:[5,3,1,""],test_remove_class_no_open_seats_removes_warnings:[5,3,1,""],test_remove_multiple_classes_no_open_seats_removes_warnings:[5,3,1,""]},"tests.utils":{TestUtils:[5,2,1,""]},flask_app:{app:[0,0,0,"-"],backend:[1,0,0,"-"],forms:[0,0,0,"-"]},tests:{conftest:[5,0,0,"-"],test_app:[5,0,0,"-"],test_courses:[5,0,0,"-"],test_schedule:[5,0,0,"-"],utils:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute"},terms:{"0":1,"10":1,"13":[],"15am":1,"200":1,"30":1,"5":[],"9am":1,"case":5,"class":[0,1,5],"default":[],"do":[],"float":1,"function":[1,5],"import":1,"int":1,"new":1,"return":[1,5],"static":[1,5],"true":1,"try":1,A:1,If:[],It:5,No:1,The:1,To:1,Will:1,__str__:[],_flaskformcsrf:[],abl:0,about:1,accept:1,activ:[],actual:0,ad:[0,1],add:[0,1],add_class:5,add_cours:1,add_registered_course_section_by_id:1,add_sect:1,addclassform:0,addit:1,addremoveform:0,addsectionform:0,after:5,alia:[],all:[0,1],allow:[],alphabet:1,alreadi:1,also:[0,5],altern:[],an:1,ani:1,api:[1,5],apiget:[1,5],apigetandparsetest:5,apipars:[1,5],app:[2,3,5],append:[],applic:1,ar:[0,1],aren:[],arg:0,argument:1,ask:1,attribut:[],avail:1,averag:[1,5],average_r:1,avg_gpa:1,back:1,backend:[0,3],bad_request:1,base:[0,1,5],befor:[1,5],bind:[],bind_field:[],blue:1,bool:1,bound:[],buffer:[],build:[],build_csrf:[],builder:1,builtin:[],bytes_or_buff:[],cache_transl:[],calcul:1,call:[1,5],can:1,can_add:1,cannot:1,caution:[],certain:0,chang:[],check_section_no_time_conflict:1,class_meet:1,class_to_add:1,classmethod:1,clear:0,clear_al:[],clearallcoursesform:0,client:5,cmsc131:1,cmsc:1,code:[1,5],color:1,combin:1,come:[],compat:[],complet:1,conftest:[2,3],consid:[],consist:[1,5],contain:1,content:[0,3],convert:1,copi:[0,1],correct:5,correspond:1,cours:[0,3,5],course_cod:1,course_credit:1,course_list:1,course_queri:[],course_raw:1,course_to_add:1,course_to_remov:1,courselist:[1,5],courselisttest:5,coursetest:5,creat:[0,5],create_app:0,credit:1,csrf:[],csrf_class:[],csrf_field_nam:[],csrf_secret:[],csrf_time_limit:[],current:[0,1],custom:[],dai:1,data:[0,5],decod:[],deconstruct:5,defaultmeta:[],defin:[],delet:[],depart:1,department_id:1,depend:5,describ:1,destruct:[],detect:[],dict:1,dictionari:1,displai:[0,1],display_serialized_schedul:[],div:[],django:[],document:[],doe:5,doesn:5,don:[],done:[],duplic:[],e:[1,5],each:1,easili:1,ed:[0,1],empti:1,emul:1,encod:[],ensur:5,equival:[],error:1,etc:[1,5],except:1,exercis:5,exist:1,expos:[],extra:[],extra_filt:[],extra_valid:[],extract:1,factori:[],fals:1,far:1,field:[],fieldnam:[],filter:[],filter_:[],fix:1,fixtur:5,flask:0,flask_app:[2,3],flask_wtf:0,flaskform:0,form:[1,2,3],format:1,formdata:[],found:1,found_cours:1,from:[0,1],frontend:1,g:[1,5],gen:[0,1],gen_:1,gene:1,genedsearchform:0,gener:[1,5],get:[1,5],get_all_professor:1,get_complete_course_by_course_cod:1,get_course_color:1,get_course_head_by_course_cod:1,get_course_heads_by_queri:1,get_course_list_by_gen_:1,get_course_list_by_page_numb:1,get_course_using_course_cod:1,get_courses_using_page_numb:1,get_formatted_weekly_schedul:1,get_professor_average_r:1,get_professor_by_nam:1,get_professor_gpa_breakdown_by_cours:1,get_review:1,get_schedule_average_gpa:1,get_sections_list_by_cours:1,get_serialized_schedul:1,get_transl:[],getdefaultencod:[],gettext:[],give:1,given:1,gotten:1,gpa:[1,5],grade:1,grades_raw:1,green:1,ha:1,handl:1,handler:[],hard:5,have:1,head:1,header:1,helper:[1,5],hidden:[],hidden_tag:[],hiddeninput:[],hook:5,how:[],html:[],i18n:[],i:1,id:1,implement:[],index:2,individu:1,info:1,infomr:1,inform:1,input:1,inputrequir:[],instanc:[],instead:[],instructor_typ:1,interact:5,interfac:[],involved_sect:1,io:1,is_submit:[],is_synchron:1,issu:1,its:1,itself:1,json:1,kei:1,kwarg:0,last:[],later:0,letter:1,list:[0,1],load:[0,1,5],load_schedul:[],load_serialized_schedul:1,local:[],locat:1,logic:5,longer:[],m:1,magenta:1,make:1,make_meeting_dict:1,map:1,match:1,matched_cours:1,max:1,maximum:1,meet:1,meetings_list:1,meetingtim:[1,5],merg:[],messag:1,meta:[],method:[1,5],methodnam:5,modul:[2,3],more:[],multi:[],multidict:[],must:[],mwf:1,myschedul:[1,5],name:1,next:[0,1],next_pag:[],nextpageonallcoursespageform:0,ngettext:[],nice:1,none:1,notabl:1,note:[],number:1,obj:[],object:[1,5],onc:[],one:[],onli:[],open:1,open_seat:1,oper:[],option:1,orang:1,order:1,other:1,otherwis:[],overlap:1,overrid:[],overridden:[],overwrit:[],packag:[2,3],page:[0,1,2],page_num:1,param:[],paramet:1,parent:1,parent_cours:1,pars:[1,5],partial:1,pass:[],patch:[],per:[],planetterp:[1,5],planetterp_course_raw_to_course_head:1,planetterp_get_course_by_course_cod:1,planetterp_get_courses_by_pag:1,planetterp_get_grades_by_course_cod:1,planetterp_get_professor_by_nam:1,planetterp_prof_raw_to_prof_head:1,planetterp_raw_grade_distribution_to_gpa:1,planetterp_search_by_queri:1,popul:[],populate_obj:[],post:[],potenti:[],preced:[],previou:0,previous:0,previous_pag:[],previouspageonallcoursespageform:0,primarili:5,procedur:1,process:[],prof_raw:1,professor:1,professor_nam:1,professor_r:1,professor_slug:1,professor_to_avg_course_gpa:1,professor_to_sect:1,properli:1,properti:[],provid:[],purpl:1,put:[],queri:1,rais:1,rate:1,raw:1,red:1,referenc:[],regist:1,relat:5,remov:[0,1],remove_all_class:1,remove_class:5,remove_cours:1,remove_registered_course_section_by_id:1,remove_sect:1,render:[],render_field:[],render_kw:[],repr:[],repres:1,represent:1,request:[1,5],requestproxi:1,requir:1,reset:1,respect:1,respons:[1,5],result:[0,1],retriev:1,review:1,rout:0,run:[],runtest:5,s:1,said:1,same:[],sampl:1,satisfi:1,schedul:[0,3,5],schedulegpa:5,scheduletest:5,schedulewarn:[1,5],schedulewarningtest:5,search:[0,1,2],search_by_gen:[],search_for_cours:[],search_queri:[],searchforcourseform:0,searchform:0,seat:1,section:[0,1,5],section_id:1,section_queri:[],section_to_add:1,section_to_remov:1,sections_raw:1,see:1,seen:1,select:0,send:1,serial:[0,1],serialize_schedul:[],serializescheduleform:0,session:[],sessioncsrf:[],set:[1,5],set_sorted_professors_by_r:1,setup:5,sever:5,shortcut:[],should:[],simpli:[],singl:1,skip:[],slot:1,slug:1,so:[1,5],some:[1,5],sort:1,specif:1,specifi:1,statu:1,str:1,str_schedul:1,strict:[],string:1,stringfield:[],style:[],subclass:[],submit:[],submitfield:[],submodul:[0,3],subpackag:[2,3],suppos:5,sy:[],t:5,tab:1,take:1,taught:1,teach:1,teardown:5,test:[1,2,3],test_add_class_and_credits_and_schedule_correct:5,test_add_class_no_open_seats_makes_warn:5,test_add_class_then_remove_class_correct_credits_and_schedul:5,test_add_duplicate_class_and_credits_and_schedule_correct:5,test_add_duplicate_course_doesnt_add_again:5,test_add_multiple_classes_no_open_seats_makes_warn:5,test_add_two_classes_correct_credits_and_schedul:5,test_add_two_classes_make_sure_ordered_by_tim:5,test_all_courses_returns_200:5,test_all_professors_returns_200:5,test_app:[2,3],test_class_formatted_weekly_schedule_correct:5,test_class_overlap_different_class_time_conflict:5,test_class_overlap_same_class:5,test_class_with_no_time_conflict:5,test_correct_average_gpa:5,test_cours:[2,3],test_course_correct_prof_rating_ord:5,test_course_correct_professor_rating_static_method:5,test_course_empty_prof_rating_ord:5,test_empty_schedule_zero_gpa:5,test_gen_ed_search_returned_courses_empty_bad_request:5,test_gen_ed_search_returned_courses_valid_good_request:5,test_get_course_color_of_course_in_schedul:5,test_get_course_color_of_course_not_in_schedul:5,test_get_course_heads_make_sure_all_courses_we_expect_are_pres:5,test_get_courses_using_course_code_invalid_course_code_throws_except:5,test_get_courses_using_course_code_valid_course_cod:5,test_get_courses_using_invalid_page_numb:5,test_get_courses_using_valid_page_numb:5,test_hashes_of_different_meetings_times_are_different_too:5,test_hashes_of_same_meetings_times_are_sam:5,test_index_returns_200:5,test_load_empty_serialized_schedul:5,test_load_serialize_schedule_work:5,test_load_serialized_schedule_invalid_cours:5,test_load_serialized_schedule_invalid_course_format:5,test_load_serialized_schedule_invalid_section_for_valid_cours:5,test_meeting_time_not_equal_to_non_meeting_time_object:5,test_meeting_times_are_equal_according_to_eq_funct:5,test_meeting_times_are_not_equal_according_to_eq_funct:5,test_mod:1,test_professor_detail_returns_200:5,test_professor_detail_returns_404_if_no_professor:5,test_professor_object_returned_valid_courselist:5,test_professor_object_returned_valid_instructor_typ:5,test_professor_object_returned_valid_nam:5,test_professor_object_returned_valid_r:5,test_remove_all_classes_on_empty_schedul:5,test_remove_all_classes_on_schedule_with_classes_in_it:5,test_remove_class_no_open_seats_removes_warn:5,test_remove_course_actually_in_schedul:5,test_remove_course_not_in_schedul:5,test_remove_multiple_classes_no_open_seats_removes_warn:5,test_removing_class_not_in_schedule_doesnt_change_credit:5,test_schedul:[2,3],test_schedule_is_empti:5,test_serialize_empty_schedul:5,test_serialize_schedule_returns_comma_separated_section_id:5,test_try_to_add_class_in_middle_of_day_start_time_overlaps_with_previous_end_tim:5,test_try_to_add_overlapping_classes_only_first_gets_ad:5,test_tutorial_returns_200:5,testcas:5,testutil:5,them:1,thi:[1,5],through:1,time:1,todo:1,tojson:1,total:1,total_seat:1,translat:[],translations_cach:[],tu:1,tupl:1,tuth:1,two:[],type:1,typic:[],umd:1,umd_io_course_raw_to_course_head:1,umd_io_sections_raw_to_section_list:1,umdio:5,umdio_get_courses_by_gen:1,umdio_get_sections_by_course_cod:1,un:[],unbound:[],unbound_field:[],unboundfield:[],unit:1,unittest:5,up:5,updat:[],update_valu:[],us:1,user:[0,1],usual:[],util:[2,3],valid:[],validate_:[],validate_on_submit:[],valu:1,version:1,view:0,viewsectionsform:0,wa:[0,1],want:1,warn:1,warning_typ:1,we:1,webob:[],week:1,weekly_schedul:1,were:1,werkzeug:[],what:[],when:1,whether:1,which:[1,5],whose:1,widget:[],within:1,without:1,wrap:[],wrap_formdata:[],wrapper:[],wtform:[],x:[],yet:1,zero:[]},titles:["flask_app package","flask_app.backend package","Welcome to UMD Schedule Builder\u2019s documentation!","team-project","run module","tests package"],titleterms:{app:0,backend:1,builder:2,conftest:5,content:[1,2],cours:1,document:2,flask_app:[0,1],form:0,indic:2,modul:[0,1,4,5],packag:[0,1,5],project:3,run:4,s:2,schedul:[1,2],submodul:1,subpackag:0,tabl:2,team:3,test:5,test_app:5,test_cours:5,test_schedul:5,umd:2,util:5,welcom:2}})