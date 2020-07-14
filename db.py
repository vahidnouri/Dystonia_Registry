# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
# import jdatetime
# import django-jalali-date  
# from django import forms
# from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
# from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.expiration = 3600 * 8  # seconds

auth.settings.extra_fields['auth_user'] = [
    Field("reception", type="boolean"),
    # Field("patient", type="boolean"),
    Field("physician", type="boolean"),
    # Field("lab", type="boolean"),
    # Field("genes", type="boolean"),
    Field("admin_", type="boolean"),
]
auth.define_tables( migrate=False )
auth.define_tables(username=False, signature=False)

auth.settings.actions_disabled = ['register']

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

genders = ["","مرد","زن"]
yes_no = ["","بلی","خیر"]
just_yes_no = ["خیر","بلی"]
just_2_yes_no = ["بلی","خیر"]
yes_no_distonia = ["","بلی","خیر","تغییر شغل به علت دیستونی"]
visit_numbers = ["","اول","دوم و بعدتر"]
off_on = ["","Off","On"]
after_before = ["","قبل از 6 عصر","بعد از 6 عصر"]
yes_no_unknown = ["نامشخص","خیر","بلی"]
suffering_nums = ["نامشخص"] +[i for i in range(10)]
distonia_distribution = ["","فوکال","همی دیستونی چپ","همی دیستونی راست","ژنرالیزه","مولتی فوکال","سگمنتال"]
distonia_activities = ["","کرامپ نویسندگان","کرامپ ورزشکاران","کرامپ تایپیست","کرامپ نوازندگان","دیستونی تکلم","سایر"]
disorder_mood = ["ندارد","ADHD","اختلالات اضطرابی","افسردگی","دوقطبی","drug abuse","اختلالات وسواسی جبر ی","اختلال پانیک","سایر","نامشخص"]
tremor_type = ["ندارد"] + ["Regular","Irregular/jerky"]
non_distonia = ["میوکلونوس","کره", "پارکینسونیسم" , "سایر"]
best_disgnosis = ["نامشخص", "combined disnonia", "primary dystonia"]
global_dist = [i for i in range(11)]
blood_type = ["","EDTA","Heparin","سایر"]
theraputic_interventions = ["","آنتی کولینرژیک","بوتولینوم توکسین", "وودوپا",'تحریک عمقی مغزی',"شل کننده عضلانی", "سایر"]



#str(list(range(0,11)))
#counsiousness = ["0","1","2","3","4","5","6","7","8","9","10"]
gait = [""] +[i for i in range(5)]  
hoehn = [""] +[i for i in range(6)]


bai = ["","0","1","2","3"]
mschwab = ["","0","10","20","30","40","50","60","70","80","90","100"]
edu_list = ["","بی سواد","ابتدایی","سیکل","دیپلم","فوق دیپلم","لیسانس","فوق لیسانس و بالاتر"]

genes = []
for i in range(1,101):
    genes.append(Field("gene_{}".format(i),"string",label="ژن {}".format(i)))
    for j in range(1,11):
        genes.append(Field("variant_{}_gene{}".format(j,i),"string",label="ژن {} واریانت {}".format(i,j)))

########## Lab Table

# jdatetime.set_locale('fa_IR')


db.define_table("principal_info",
    Field("f_name", "string",label="نام و نام خانوادگی"),
    Field("reception_id", "string",label="کد ملی", required=True),  

    #migrate = False,    
    fake_migrate=True,
    )
# -----------------------Reception Section ------------------------------
db.principal_info.reception_id.requires=IS_NOT_IN_DB(db,'principal_info.reception_id')
db.define_table("reception_section", 
#    Field("f_name", "string",label="نام و نام خانوادگی"),
    Field("reception_id", "string",label="کد پذیرش", writable=False, readable = False),
    Field("gender", requires=IS_IN_SET(genders, zero=None),label="جنسیت"),

    # Field("birth_date_day", format = jdatetime.datetime.now().strftime('%A %B'),label="تاریخ تولد"),
    # Field("birth_date_day", "string",label="روز تولد"),
    # Field("birth_date_month", "string",label="ماه تولد"),
    # Field("birth_date_year", "string",label="سال تولد"),
    Field("birth_date_date", "date",label="تاریخ تولد"),
    # Field("visit_date_day", "string",label="روز ویزیت"),
    # Field("visit_date_month", "string",label="ماه ویزیت"),
    # Field("visit_date_year", "string",label="سال ویزیت"),    
    Field("visit_date", "date",label="تاریخ ویزیت"),    
    Field("id_code", "string",label="کد ملی"),
    Field("tel", "string",label=" تلفن ثابت"),
    Field("mobile", "string",label="شماره موبایل"),
    Field("city", "string",label="شهر"),
    Field("address", "text",label="محل سکونت"),
    Field("e_mail", "string",label="ایمیل"),
    Field("insurance_type", "string",label="نوع بیمه"),
    Field("education", requires=IS_IN_SET(edu_list, zero=None),label="تعداد سالهای تحصیل رسمی"),
    Field("career", "string",label="شغل"),
    Field("pedigree_file", "upload",label="بارگذاری تصویر شجره ",
          uploadfolder='C:/Web2Py/applications/dystonia/static/images',uploadseparate=True
          ), 
    migrate = False,)

#-------------------- Physician Section -------------------------------

db.define_table("physician_section",
    Field("reception_id", "string",label="کد پذیرش", writable=False, readable = False),
    #Field("updr", "string",label="UPDRS"),

    Field("change_work", requires=IS_IN_SET(yes_no_distonia, zero=None),label="?از کار افتادگی به علت دیستونی"),
    Field("working", requires=IS_IN_SET(yes_no, zero=None),label="?بیمار هم اکنون مشغول به کار است"),
    Field("income", "string",label=" درآمد متوسط ماهیانه به تومان"),
    Field("visit_times", requires=IS_IN_SET(visit_numbers, zero=None),label="نوبت ویزیت"),
    Field("distonia_family_bkgrnd", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" سابقه دیستونی در خانواده"),   
    Field("mother", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" مادر مبتلا"),   
    Field("father", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" پدر مبتلا"),   
    Field("suffering_br_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد برادر مبتلا"),   
    Field("suffering_sis_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد خواهر مبتلا"), 
    Field("healthy_br_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد برادر سالم"),   
    Field("healthy_sis_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد خواهر سالم"), 
    Field("kids_num", "string",label="تعداد فرزندان"),
    Field("healthy_daughter_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد دختر سالم"), 
    Field("suffering_daughter_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد دختر مبتلا"), 
    Field("healthy_son_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد پسر سالم"),   
    Field("suffering_son_nums", requires=IS_IN_SET(suffering_nums, zero=None),label=" تعداد پسر مبتلا"),   
    Field("family_tremor_bkgrnd", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" سابقه ترمور در خانواده"),   
    Field("family_myoclonus_bkgrnd", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" سابقه میوکلونوس در خانواده"),   
    Field("family_parkinson_bkgrnd", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" سابقه پارکینسون یا پارکینسونیسم در خانواده"),   
    Field("family_others_bkgrnd", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" سابقه سایر بیماریها در خانواده"),   
    Field("disease_type", "string",label="نوع بیماری"),
    # Field("sickness_start_day", "string",label="روز شروع علائم"),
    # Field("sickness_start_month", "string",label="ماه شروع علائم"),
    # Field("sickness_start_year", "string",label="سال شروع علائم"),
    Field("sickness_start_date", "date",label="تاریخ شروع علائم"),
    # Field("diagnostic_day", "string",label="روز تشخیص بیماری"),
    # Field("diagnostic_month", "string",label="ماه تشخیص بیماری"),
    # Field("diagnostic_year", "string",label="سال تشخیص بیماری"),
    Field("diagnostic_date", "date",label="تاریخ تشخیص بیماری"),
    Field("distonia_dist", requires=IS_IN_SET(distonia_distribution, zero=None),label=" توزیع فعلی دیستونی"),   
    Field("task_specific", requires=IS_IN_SET(yes_no, zero=None),label=" task specific distonia"),   
    Field("dist_activities", requires=IS_IN_SET(distonia_activities, zero=None),label=" نوع فعالیت منجر به دیستونی"),   
    Field("task_specific_type", "string",label="task specific نوع دیستونی"),
    Field("dist_less_than_a_week", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" شروع ناگهانی دیستونی در کمتر از یک هفته"),   
    Field("disorder_mood_exist", requires=IS_IN_SET(disorder_mood, zero=None),label=" وجود اختلال خلقی"),   
    Field("disorder_mood_type", "string",label="نوع اختلال خلقی"),
    Field("concept_disorder", requires=IS_IN_SET(yes_no_unknown, zero=None),label=" وجود اختلال شناختی"),   

    ## محل شروع دیستونی سر تیتر اضافه شود

    Field("lfoot", requires=IS_IN_SET(just_yes_no, zero=None),label="Left foot"),   
    Field("rfoot", requires=IS_IN_SET(just_yes_no, zero=None),label="Right foot"),   
    Field("luleg", requires=IS_IN_SET(just_yes_no, zero=None),label="Left upper leg"),   
    Field("ruleg", requires=IS_IN_SET(just_yes_no, zero=None),label="Right upper leg"),   
    Field("lhand", requires=IS_IN_SET(just_yes_no, zero=None),label="Left hand"),   
    Field("rhand", requires=IS_IN_SET(just_yes_no, zero=None),label="Right hand"),   
    Field("luarm", requires=IS_IN_SET(just_yes_no, zero=None),label="Left upper arm"),   
    Field("ruarm", requires=IS_IN_SET(just_yes_no, zero=None),label="Right upper arm"),   
    Field("lshoulder", requires=IS_IN_SET(just_yes_no, zero=None),label="Left shoulder"),   
    Field("rshoulder", requires=IS_IN_SET(just_yes_no, zero=None),label="Right shoulder"),   
    Field("luface", requires=IS_IN_SET(just_yes_no, zero=None),label="Left upper face"),   
    Field("Ruface", requires=IS_IN_SET(just_yes_no, zero=None),label="Right upper face"),   
    Field("llface", requires=IS_IN_SET(just_yes_no, zero=None),label="Left lower face"),   
    Field("rlface", requires=IS_IN_SET(just_yes_no, zero=None),label="Right lower face"),   
    Field("pelvis", requires=IS_IN_SET(just_yes_no, zero=None),label="Pelvis"),   
    Field("neck", requires=IS_IN_SET(just_yes_no, zero=None),label="Neck"),   
    Field("trunk", requires=IS_IN_SET(just_yes_no, zero=None),label="Trunk"),   
    Field("jaw", requires=IS_IN_SET(just_yes_no, zero=None),label="Jaw"),   
    Field("larynx", requires=IS_IN_SET(just_yes_no, zero=None),label="Larynx"),   
    Field("tongue", requires=IS_IN_SET(just_yes_no, zero=None),label="Tongue"),   
    Field("fix_dist", requires=IS_IN_SET(yes_no_unknown, zero=None),label="شروع با دیستونی فیکس"),   

    ## توزیع و نوع ترمور سر تیتر اضافه شود

    Field("no_tremor", requires=IS_IN_SET(just_yes_no, zero=None),label="آیا ترمور دارد"),
    Field("t_lfoot", requires=IS_IN_SET(tremor_type, zero=None),label="Left foot"),   
    Field("t_rfoot", requires=IS_IN_SET(tremor_type, zero=None),label="Right foot"),   
    Field("t_luleg", requires=IS_IN_SET(tremor_type, zero=None),label="Left upper leg"),   
    Field("t_ruleg", requires=IS_IN_SET(tremor_type, zero=None),label="Right upper leg"),   
    Field("t_lhand", requires=IS_IN_SET(tremor_type, zero=None),label="Left hand"),   
    Field("t_rhand", requires=IS_IN_SET(tremor_type, zero=None),label="Right hand"),   
    Field("t_luarm", requires=IS_IN_SET(tremor_type, zero=None),label="Left upper arm"),   
    Field("t_ruarm", requires=IS_IN_SET(tremor_type, zero=None),label="Right upper arm"),   
    Field("t_lshoulder", requires=IS_IN_SET(tremor_type, zero=None),label="Left shoulder"),   
    Field("t_rshoulder", requires=IS_IN_SET(tremor_type, zero=None),label="Right shoulder"),   
    Field("t_luface", requires=IS_IN_SET(tremor_type, zero=None),label="Left upper face"),   
    Field("t_Ruface", requires=IS_IN_SET(tremor_type, zero=None),label="Right upper face"),   
    Field("t_llface", requires=IS_IN_SET(tremor_type, zero=None),label="Left lower face"),   
    Field("t_rlface", requires=IS_IN_SET(tremor_type, zero=None),label="Right lower face"),   
    Field("t_pelvis", requires=IS_IN_SET(tremor_type, zero=None),label="Pelvis"),   
    Field("t_neck", requires=IS_IN_SET(tremor_type, zero=None),label="Neck"),   
    Field("t_trunk", requires=IS_IN_SET(tremor_type, zero=None),label="Trunk"),   
    Field("t_jaw", requires=IS_IN_SET(tremor_type, zero=None),label="Jaw"),   
    # Field("t_larynx", requires=IS_IN_SET(tremor_type, zero=None),label="Larynx"),   
    Field("t_tongue", requires=IS_IN_SET(tremor_type, zero=None),label="Tongue"),   
    

    Field("tremor_bf_dist", requires=IS_IN_SET(yes_no_unknown, zero=None),label="شروع ترمور قبل از شروع دیستونی"),   
    Field("pain_in_dist", requires=IS_IN_SET(yes_no_unknown, zero=None),label="وجود درد درتوزیع دیستونی"),   
    Field("pain_in_dist", requires=IS_IN_SET(non_distonia, zero=None),label="سایر اختلالات غیر دیستونی"),  
    Field("disorder_type", "string",label="سایر اختلالات غیر دیستونی"),
    Field("best_distonia_diag", requires=IS_IN_SET(best_disgnosis, zero=None),label="بهترین تشخیص بالینی"),

    # If primary distonia is selected:
    Field("ns_pd", requires=IS_IN_SET(just_yes_no, zero=None),label="Not specified"),   
    Field("cervical_dystonia", requires=IS_IN_SET(just_yes_no, zero=None),label="Cervical dystonia"),  
    Field("blepharospasm", requires=IS_IN_SET(just_yes_no, zero=None),label="Blepharospasm"),  
    Field("lingual", requires=IS_IN_SET(just_yes_no, zero=None),label="Lingual"),  
    Field("U_l_f", requires=IS_IN_SET(just_yes_no, zero=None),label="Upper and lower facial"),  
    Field("abductor", requires=IS_IN_SET(just_yes_no, zero=None),label="Laryngeal (abductor)"),  
    Field("adductor", requires=IS_IN_SET(just_yes_no, zero=None),label="Laryngeal (adductor)"),  
    Field("mixed", requires=IS_IN_SET(just_yes_no, zero=None),label="Laryngeal (mixed)"),  
    Field("l_e", requires=IS_IN_SET(just_yes_no, zero=None),label="Lower extremity"),  
    Field("u_e", requires=IS_IN_SET(just_yes_no, zero=None),label="Upper extremity"),  
    Field("generalized", requires=IS_IN_SET(just_yes_no, zero=None),label="Generalized"),  


    Field("sensory_trick", requires=IS_IN_SET(yes_no_unknown, zero=None),label="sensory trick:وجود دارد"),   
    Field("sensory_trick_explanation", "text",label="sensory trick explanation"),   

    # Paraclinic Actions Title
    # Add fields for uploading files
    Field("mri", requires=IS_IN_SET(just_yes_no, zero=None),label="MRI"), 
    Field("dscr_mri", "text",label="MRI نتایج"), 
    # Field("mri_pic_path", "string",label="مسیر عکس ها"), 
    Field("mri_pic_file", "upload",label="بارگذاری تصویر ام آر آی ",
          uploadfolder='C:/Web2Py/applications/dystonia/static/images',uploadseparate=True),

    Field("ct_scan", requires=IS_IN_SET(just_yes_no, zero=None),label="CT Scan"), 
    Field("dscr_ct_scan", "text",label="CT Scan نتایج"), 
    # Field("ct_scan_pic_path", "string",label="مسیر عکس ها"), 
    Field("ct_scan_pic_file", "upload",label="بارگذاری تصویر سی تی اسکن ",
          uploadfolder='C:/Web2Py/applications/dystonia/static/images',uploadseparate=True),    
    
    Field("tests", requires=IS_IN_SET(just_yes_no, zero=None),label="آزمایش‌ها"),
    Field("dscr_tests", "text",label="نتایج آزمایش‌ها"), 
    # Field("tests_pic_path", "string",label="مسیر عکس ها"), 
    Field("tests_pic_file", "upload",label="بارگذاری تصویر آزمایش‌ها ",
          uploadfolder='C:/Web2Py/applications/dystonia/static/images',uploadseparate=True),    


    Field("refer", requires=IS_IN_SET(just_yes_no, zero=None),label="مشاوره یا ارجاع"),  
    Field("dscr_refer", "text",label="نتایج مشاوره یا ارجاع"), 
    Field("councelling_pic_file", "upload",label="بارگذاری تصویر مشاوره ",
          uploadfolder='C:/Web2Py/applications/dystonia/static/images',uploadseparate=True),  
    

    Field("other_fs", requires=IS_IN_SET(just_yes_no, zero=None),label="سایر"),  
    Field("dscr_others", "text",label="نتایج سایر"), 


    Field("theraputic_intervention_1", requires=IS_IN_SET(theraputic_interventions, zero=None),label="اقدامات درمانی 1"), 
    Field("theraputic_int_1_others", "string",label="نام دارو"),
    Field("theraputic_intervention_2", requires=IS_IN_SET(theraputic_interventions, zero=None),label="اقدامات درمانی 2"), 
    Field("theraputic_int_2_others", "string",label="نام دارو"),
    


    # FM  نتیجه بررسی معیار فان- مارسدن 

    Field("eye_fac", "string",label="چشم فاکتور ایجاد کننده"), 
    Field("eye_int", "string",label="چشم شدت"), 
    Field("eye_sum", "string",label="حاصل"), 
    Field("mouth_fac", "string",label="دهان فاکتور ایجاد کننده"), 
    Field("mouth_int", "string",label="دهان شدت"), 
    Field("mouth_sum", "string",label="حاصل"), 
    Field("eat_fac", "string",label="بلع فاکتور ایجاد کننده"), 
    Field("eat_int", "string",label="بلع شدت"), 
    Field("eat_sum", "string",label="حاصل"), 
    Field("neck_fac", "string",label="گردن فاکتور ایجاد کننده"), 
    Field("neck_int", "string",label="گردن شدت"), 
    Field("neck_sum", "string",label="حاصل"), 
    Field("rhand_fac", "string",label="دست راست فاکتور ایجاد کننده"), 
    Field("rhand_int", "string",label="دست راست شدت"), 
    Field("rhand_sum", "string",label="حاصل"), 
    Field("lhand_fac", "string",label="دست چپ فاکتور ایجاد کننده"), 
    Field("lhand_int", "string",label="دست چپ شدت"), 
    Field("lhand_sum", "string",label="حاصل"), 
    Field("body_fac", "string",label="تنه فاکتور ایجاد کننده"), 
    Field("body_int", "string",label="تنه شدت"), 
    Field("body_sum", "string",label="حاصل"), 
    Field("rleg_fac", "string",label="پای راست فاکتور ایجاد کننده"), 
    Field("rleg_int", "string",label="پای راست شدت"), 
    Field("rleg_sum", "string",label="حاصل"),     
    # Field("lleg_fac", "string",label=" هدننک داجیا روتکاف پچ یاپ"),          
    Field("lleg_fac", "string",label=" پای چپ فاکتور ایجاد کننده"),          
    Field("lleg_int", "string",label="پای چپ شدت"), 
    Field("lleg_sum", "string",label="حاصل"),
    Field("fm_total", "string",label="مجموع نمره"),

   # مقیاس گلوبال نمره دهی شدت دیستونی   

    Field("eye_top_face", requires=IS_IN_SET(global_dist, zero=None),label="چشم و بالای صورت"), 
    Field("bottom_face", requires=IS_IN_SET(global_dist, zero=None),label="پایین صورت"), 
    Field("g_tongue", requires=IS_IN_SET(global_dist, zero=None),label="فک و زبان"), 
    Field("g_larynx", requires=IS_IN_SET(global_dist, zero=None),label="حنجره"), 
    Field("g_neck", requires=IS_IN_SET(global_dist, zero=None),label="گردن"), 
    Field("g_rshoulder", requires=IS_IN_SET(global_dist, zero=None),label="شانه و پروگزیمال بازو راست"), 
    Field("g_lshoulder", requires=IS_IN_SET(global_dist, zero=None),label="شانه و پروگزیمال بازو چپ"), 
    Field("relbow", requires=IS_IN_SET(global_dist, zero=None),label="دیستال بازو، دست و آرنج راست"), 
    Field("lelbow", requires=IS_IN_SET(global_dist, zero=None),label="دیستال بازو، دست و آرنج چپ"), 
    Field("rplc", requires=IS_IN_SET(global_dist, zero=None),label="پلویس و پروگزیمال پای راست"), 
    Field("lplc", requires=IS_IN_SET(global_dist, zero=None),label="پلویس و پروگزیمال پای چپ"), 
    Field("rdist", requires=IS_IN_SET(global_dist, zero=None),label="دیستال پا و زانوی راست"), 
    Field("ldist", requires=IS_IN_SET(global_dist, zero=None),label="دیستال پا و زانوی چپ"), 
    Field("body", requires=IS_IN_SET(global_dist, zero=None),label="تنه"), 
    Field("global_total", "string",label="مجموع نمره"),

    Field("film_upload", "upload",label="بارگذاری فایل زیپ شده‌ی فیلم‌ها ",
            uploadfolder='C:/Web2Py/applications/dystonia/static/films',uploadseparate=True, 
          ),           
    
    Field("fill_by", 'string',label="تکمیل کننده"),  

    migrate = False,
    
    fake_migrate = True,
    )
db.define_table("lab_section", 
    Field("reception_id", "string",label="کد پذیرش", writable=False, readable = False),
    Field("lab_2", requires=IS_IN_SET(blood_type, zero=None),label="خون"),
    Field("lab_part", "string",label=" سایر"),
    Field("lab_1", requires=IS_IN_SET(yes_no, zero=None),label=" DNA استخراج"),    
    Field("lab_3", "string",label="حجم خون باقیمانده"),
    Field("lab_4", "string",label="روش"),
    Field("lab_5", "string",label="DNA غلظت"),    
    Field("lab_6", "string",label="DNA حجم میکرولیتر"),
    migrate = False,
    fake_migrate = True,
    )

db.define_table("genes_table",Field("project", "string",label="Project"),Field("reception_id", "string",label="کد پذیرش", writable=False, readable = False),*genes[0:110],migrate = False,fake_migrate = True)
