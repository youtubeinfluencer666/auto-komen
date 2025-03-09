from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import random
import json

#Reshaper
def baca_komentar_dari_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def random_delay(min_delay=0.5, max_delay=2):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-webgl")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--silent")
    options.add_argument("--disable-ffmpeg")
    options.add_argument("--disable-logging")
    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(100)
    return driver

def find_element_by_multiple_attributes(driver, tag_name, attributes):
    for attribute in attributes:
        try:
            return WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"{tag_name}[{attribute}]"))
            )
        except TimeoutException:
            continue
    return None

def dofollow(urls, komentar_file):
    driver = init_driver()
    data_komentar = baca_komentar_dari_file(komentar_file)

    for url in urls:
        try:
            # Buka URL
            driver.get(url)

            # Pilih data komentar secara acak
            komentar_terpilih = random.choice(data_komentar)

            # Isi form komentar
            # Komentar
            komentar_field = find_element_by_multiple_attributes(driver, 'textarea', ['data-sf-role=comments-new-message', 'placeholder=Leave a comment'])
            if komentar_field:
                random_delay(2, 4)
                komentar_field.clear()
                random_delay()
                komentar_field.send_keys(komentar_terpilih["komentar"])
            
            # Nama
            nama_field = find_element_by_multiple_attributes(driver, 'input', ['data-sf-role=comments-new-name', 'placeholder=Your name'])
            if nama_field:
                nama_field.clear()
                random_delay()
                nama_field.send_keys(komentar_terpilih["nama"])

            # Email
            email_field = find_element_by_multiple_attributes(driver, 'input', ['data-sf-role=comments-new-email', 'placeholder=Email (optional)'])
            if email_field:
                email_field.clear()
                random_delay()
                email_field.send_keys(komentar_terpilih["email"])

            # Klik tombol submit
            try:
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-sf-role="comments-new-submit-button"]'))
                )
                random_delay()
                submit_button.click()
                print(f"Komentar berhasil > {url}")
            except TimeoutException:
                print(f"Komentar Gagal > {url}")

            # Tunggu beberapa detik untuk memastikan pengiriman
            time.sleep(3)

        except WebDriverException:
            print(f"Terjadi Kesalahan > {url}")
            continue

    driver.quit()
    print("Semua URL Dofollow Telah Selesai Diproses.")

def nofollow(urls, komentar_file):
    driver = init_driver()
    data_komentar = baca_komentar_dari_file(komentar_file)

    for url in urls:
        try:
            # Buka URL
            driver.get(url)

            # Pilih data komentar secara acak
            komentar_terpilih = random.choice(data_komentar)

            # Mencari form komentar
            komentar_section = find_element_by_multiple_attributes(driver, 'form', ['id=comment', 'class=comment-form', 'name=comment'])
            if not komentar_section:
                print(f"Tidak Ada Form Komentar > {url}")
                continue

            # Isi form komentar
            # Nama
            nama_field = find_element_by_multiple_attributes(driver, 'input', ['id=author', 'name=author', 'class=name'])
            if nama_field:
                nama_field.clear()
                random_delay()
                nama_field.send_keys(komentar_terpilih["nama"])

            # Email
            email_field = find_element_by_multiple_attributes(driver, 'input', ['id=email', 'name=email', 'class=email'])
            if email_field:
                email_field.clear()
                random_delay()
                email_field.send_keys(komentar_terpilih["email"])

            # Website
            website_field = find_element_by_multiple_attributes(driver, 'input', ['id=url', 'name=url', 'class=website'])
            if website_field:
                website_field.clear()
                random_delay()
                website_field.send_keys(komentar_terpilih["website"])

            # Komentar
            komentar_field = find_element_by_multiple_attributes(driver, 'textarea', ['id=comment', 'name=comment', 'class=comment'])
            if komentar_field:
                komentar_field.clear()
                random_delay()
                komentar_field.send_keys(komentar_terpilih["komentar"])

            # Klik tombol submit
            submit_button = find_element_by_multiple_attributes(driver, 'input', ['id=submit', 'name=submit', 'type=submit', 'class=submit'])
            if not submit_button:
                submit_button = find_element_by_multiple_attributes(driver, 'button', ['type=submit', 'class=submit', 'id=submit'])

            if submit_button:
                submit_button.click()
                print(f"Komentar berhasil > {url}")
            else:
                print(f"Komentar Gagal > {url}")

            # Tunggu beberapa detik untuk memastikan pengiriman
            time.sleep(3)

        except WebDriverException:
            print(f"Terjadi Kesalahan > {url}")
            continue

    driver.quit()
    print("Semua URL Nofollow Telah Selesai Diproses.")

def main():
    print("Pilih Jenis Komentar:")
    print("1. Dofollow")
    print("2. Nofollow")
    pilihan = input("Masukkan Pilihan (1 atau 2): ").strip()

    if pilihan == "1":
        urls = [
            "https://appeals.cuyahogacounty.gov/about-us/judges/judge-sean-c-gallagher/eighth-district-court-of-appeals",
            "https://bebasata.qnb.com.eg/transfers/Gold-debit-becard",
            "https://conwayintranet.mhpteamsi.com/home/conway-regional/2021/03/01/ay-magazine%27s-best-of-2021?",
            "https://flvs.net/student-parent-resources/current-students/flex-webinars/2021/11/02/counselor-webinars/school-counselor-minute-home-education-graduation",
            "https://flvs.net/student-parent-resources/current-students/flex-webinars/2023/01/11/counselor-webinars/new-to-home-education-informational-webinar",
            "https://food.ussoy.org/news/media-resources/high-oleic-soybean-oil-leaves-cronuts-perfectly-flaky",
            "https://haugkubota.com/about/staff/haug-kubota-llc/lee-johnson",
            "https://lacrossecounty.org/services/marriage-licenses",
            "https://lacrossecounty.org/services/marriage-records",
            "https://masterbee.itu.edu.tr/haberler/2022/04/01/masterbee-basvuru-yeniden-acildi",
            "https://northwesternenergy.com/about-us/helping-create-a-bright-future/bright-stories-community-vitality#",
            "https://ntlifts.com/equipment/skyjack/skyjack/rt-scissor-lifts",
            "https://ntlifts.com/home/giant",
            "https://riverparksouth.qualicocommunities.com/homes/gallery/images/librariesprovider19/homesgallery/rps-2",
            "https://sr.kaust.edu.sa/blog/just-a-little-everyday-sr-/2020/10/09/so-long-single-use-plastics",
            "https://thecma.ca/media/canada-post",
            "https://www-dr.fscj.edu/discover/humanresources/current-employees/compensation-classification/classificationlist",
            "https://www-uat.fscj.edu/discover/humanresources/current-employees/compensation-classification/classificationlist",
            "https://www.aacom.org/news-reports/press-releases/2022/06/30/osteopathic-medical-community-urges-further-discussion-and-understanding-about-distinctive-licensure-assessment-of-do-and-md-students",
            "https://www.aam.com/contact/aftermarket",
            "https://www.aam.com/contact/corporate-communications",
            "https://www.aam.com/media/christopher-son",
            "https://www.associationforjewishstudies.org/about-ajs/press-room/news-events/events-detail/2023/02/23/default-calendar/b%27nai-binge-streaming-programming-list-for-february-22-by-laurie-baron-and-beth-chernoff",
            "https://www.athenscollege.edu.gr/en/adult-learning/adult-education-program/2022/06/13/%CF%80%CF%81%CF%8C%CE%B3%CF%81%CE%B1%CE%BC%CE%BC%CE%B1-%CE%B5%CE%BD%CE%B7%CE%BB%CE%AF%CE%BA%CF%89%CE%BD---events/feast-of-the-holy-spirit-%28school-closed%29",
            "https://www.blackbox.com/gsi-forms/thank-you-ucc-premise-cloud-hybrid-whitepaper/real-time-smart-provider-education-communication",
            "https://www.calcities.org/home/resources/advancing-equity/2021/03/24/cal-cities-embarks-on-governance-evaluation-to-enhance-engagement-effectiveness-and-inclusivity",
            "https://www.capitalfarmcredit.com/farming/crop-insurance",
            "https://www.capmetro.org/majorprojects/downtown-station",
            "https://www.capmetro.org/majorprojects/electric-fleet",
            "https://www.carlisleevents.com/media/news-articles/2018/03/01/2018-infiniti-qx80-three-ton-luxury-suv-continues-its-evolution",
            "https://www.corenetglobal.org/about-corenet-global/news/2024/01/29/96--of-commercial-real-estate-firms-have-dei-strategies--firms-increasingly-focus-on-scholarships-and-internships",
            "https://www.csa.gov.sg/News-Events/events/upcoming-events/2024/03/02/default-calendar/be-cyber-safe-workshop-for-seniors",
            "https://www.familylaw.co.uk/contact/event-sponsorship",
            "https://www.fao.org/emergencies/our-focus/social-protection/yemen-land-sea-airwaves-livelihood-specific-covid-19-sensitization/fr",
            "https://www.flvs.net/student-parent-resources/current-students/flex-webinars/2021/11/02/counselor-webinars/school-counselor-minute-home-education-graduation",
            "https://www.fscj.edu/discover/humanresources/current-employees/compensation-classification/classificationlist",
            "https://www.fslso.com/education-events/news/2024/08/08/florida-gov.-desantis-assesses-hurricane-debby-damage-launches-activate-hope-for-recovery-resources",
            "https://www.fslso.com/education-events/news/2024/08/21/surplus-lines-depopulation-participation-and-its-impact-on-non-primary-residences",
            "https://www.heliar.com/es-ar/home/blog---callout",
            "https://www.illinoismutual.com/about-us/illinois-mutual-in-the-community",
            "https://www.illinoismutual.com/agent-resources/training/di-agent-training-videos/di-training---cross-selling-life-insurance-with-di",
            "https://www.janes.com/about/our-purpose/leadership-values/rob-veal",
            "https://www.janes.com/about/our-purpose/our-intelligence-advisors/jan-broeks",
            "https://www.jblearning.com/events/2022/11/06/default-calendar/apha-annual-meeting---150th-anniversary",
            "https://www.keystonetitleservices.com/realsource-demo/2020/11/24/9-Easy-Ways-to-Increase-Social-Media-Engagement",
            "https://www.lakeshore.com/home/common-mode-artifacts-in2d-materials-with-significant-contact-resistance?srsltid=AfmBOop9s4XaaE-2F75ncZuLk8nRqg3-DZFr0Ovgr0JXSXA3J-NaG29M",
            "https://www.marshallcavendish.com/our-books/categories/9789815044126",
            "https://www.modalshop.com/calibration/learn/triaxial-accelerometer-review",
            "https://www.modalshop.com/rental/learn/sound-level-meter-software-solutions",
            "https://www.mychildsmuseum.org/education/school-programs/stuffee",
            "https://www.mychildsmuseum.org/education/school-programs/super-planet-heroes",
            "https://www.ncbfaa.org/home/2030/04/28/ncbfaa-conferences/ncbfaa-annual-meeting",
            "https://www.ntplc.co.th/contact-us/about-nt",
            "https://www.ntplc.co.th/contact-us/online-services",
            "https://www.nusenda.org/whb-welcome/eguide-library/business-mobile-and-internet-banking",
            "https://www.odcec.mi.it/home/2021/01/27/age.-ordinanza-del-sindaco-di-milano-del-23-gennaio-2021.-modifica-orari-di-apertura-al-pubblico",
            "https://www.parent.edu.hk/en/smart-parent-net/education-bureau",
            "https://www.parent.edu.hk/en/smart-parent-net/healthy-school-policy",
            "https://www.parent.edu.hk/en/smart-parent-net/integrated-education-and-special-education-information-online",
            "https://www.pcmc.com/fr/events/2018/02/06/default-calendar/converters-expo-south",
            "https://www.pianational.org/home/contact",
            "https://www.princegeorgescfcu.org/test/06test-bop",
            "https://www.qualico.com/home/2021/01/18/exponential-growth-in-2020-for-pacesetter-homesdallas-fort-worth",
            "https://www.scapahealthcare.com/home/healthcare/2020/11/10/scapa-healthcare-portfolio-of-skin-adhesives-and-topical-solutions-for-diabetic-patients",
            "https://www.scdf.gov.sg/join-us/career-outreach-activities/2024/05/23/career-outreach-activities/tampines-jc-cshe-fair",
            "https://www.sjchs.org/a-z-services-list/institute-for-advanced-bone-and-joint-surgery/dr.-katherine-bebeau",
            "https://www.stockmanbank.com/help/frequently-asked-questions/how-do-i-enroll-in-text-message-banking",
            "https://www.technicair.com/home/2019/10/23/signature-technicair-introduces-new-website-and-technical-article-portal",
            "https://www.tellmfg.com/solutions/commercial-construction/lc2600-series-lock",
            "https://www.texasamerican.com/class-listing/unlocking-th-epower-of-ai---a-game-changer-for-realtors--12.12.2024",
            "https://www.townofsurfsidefl.gov/news-and-events/events-list/2024/03/10/events/music-on-the-beach",
            "https://www.townofsurfsidefl.gov/news-and-events/events-list/2024/04/14/events/music-on-the-beach",
            "https://www.virginiaheart.com/for-patients/patient-testimonials/curt's-story--sleep-apnea",
            "https://www.virginiaheart.com/for-patients/patient-testimonials/vince%27s-story--congestive-heart-failure",
            "https://www.vongahlen.com/home/Reference-RTM-Nijmegen-",
            "https://www.warealtor.org/about-us/contact-us/officers-leadership2024/jeff-smart-2024",
            "https://www.wayne-dalton.com/commercial/dock-equipment/mechanical-pit-leveler/the-value-of-our-daltondock-equipment",
            "https://www.wcu.com/your-life/meet-the-insurance-team/laura-wellington-o'neil",
            "https://www.worldgovernmentsummit.org/observer/articles/2022/worsening-conflict-environment",
            "https://www.turkcebilgi.com/antiller",
            "https://www.lemondeducampingcar.fr/equipement/accessoires-equipement/pour-ou-contre-le-frigo-tout-electrique-dans-les-camping-cars-avis-dutilisateurs/189856",
            "https://www.hcihealthcare.ng/2020/09/11/jedi-jedi-and-you/",
            "http://fourloop.s11.xrea.com/blosxom/index.cgi/music/DieselUMusic.comments",
            "http://www.jardinage.eu/article/taille-d-un-tilleul-1196",
        ]
        dofollow(urls, "dofollow.json")
        
    elif pilihan == "2":
        urls = [
            "https://www.ub.edu/multilingua/resultats-de-la-matricula-de-rosetta-stone/",
            "https://www.ocf.berkeley.edu/~paultkim/will-kobo-release-a-forma-2-in-2020/",
            "https://www.mae.gov.bi/en/visit-to-burundi-of-a-delegation-from-the-african-union-commission/",
            "https://www.derechoclaro.der.unicen.edu.ar/index.php/2018/03/28/ut-enim-ad-minima-veniam-ullam-corporis-suscipit-laboriosam/",
            "https://wordpress.morningside.edu/tajaprince13/2015/11/05/news-comment-10/",
            "http://schmitz.environment.yale.edu/blog/changing-the-conversation-about-renewable-energy-development-and-conservation#comments",
            "https://moveme.studentorg.berkeley.edu/project/standwithhongkong/",
            "https://uwb.ds.lib.uw.edu/supportallstudents/uncategorized/centro-rendu-saint-vincent-de-paul/",
            "https://student.uog.edu.et/working/",
            "https://slice.uccs.edu/?p=752",
            "https://seu.unju.edu.ar/?p=4948",
            "https://programas.cooperativa.cl/dulcepatria/2011/05/30/30-chilenos-semana-14-lunes-30-de-mayo-al-5-de-junio/",
            "https://scmhrd.edu/corporate-excellece-awards-2023/",
            "https://sci.oouagoiwoye.edu.ng/2018/05/15/programme-philosophy-and-objectives/",
            "https://scholarblogs.emory.edu/onlineteachingsp2015/2015/03/20/dever-module-8-udl-yes-and-no/#comments",
            "https://rmik.poltekkes-smg.ac.id/?p=931",
            "https://rmik.poltekkes-smg.ac.id/?p=359",
            "https://proint.uea.edu.br/2023/02/27/projeto-de-extensao-a-revitalizacao-da-biblioteca-publica-do-careiro-castanho-clube-de-leitura-e-valorizacao-dos-escritores-regionais/",
            "https://proex.uea.edu.br/2024/05/08/congraeso/",
            "https://patricellilab.faculty.ucdavis.edu/2014/12/15/congratulations-conor/",
            "https://openlab.bmcc.cuny.edu/che121-202l-fall-2020/2020/06/17/welcome/",
            "https://odon.edu.uy/sitios/uae/galeria-multimedia/img_1489/",
            "https://odon.edu.uy/sitios/materialesdentales/2017/06/29/hola-mundo/",
            "https://newinti.edu.my/inews/link-post-format/",
            "https://med.aswu.edu.eg/en/news/the-south-korean-ambassador-visits-the-faculty-of-al-alsun/",
            "https://mae.gov.bi/diaspora/2023/07/05/la-diaspora-burundaise-de-norvege-celebre-le-61eme-anniversaire-de-lindependance-du-burundi/",
            "https://linguistik-sps.upi.edu/?p=1509",
            "https://joventic.uoc.edu/poder-sentarme-y-hacer-un-programa/paret_305x350/",
            "https://joventic.uoc.edu/poder-sentarme-y-hacer-un-programa/jugant_305x350/",
            "https://fsu.edu.in/uncategorized/guest-lecture-by-dr-bhanu-pratap-singh-consultant-ent-and-head-neck-surgeon/",
            "https://feettothefire.blogs.wesleyan.edu/2009/02/19/opening-night/",
            "https://eq-ccqqfar.usac.edu.gt/veranos-de-investigacion-cientifica-universidad-de-guanajuato-mexico-2020/",
            "https://eportfolios.macaulay.cuny.edu/lutton17/2017/02/10/comment-on-a-post/comment-page-83/#comment-93441",
            "https://eportfolios.macaulay.cuny.edu/lutton17/2017/02/10/comment-on-a-post/comment-page-77/",
            "https://education.ssru.ac.th/%E0%B8%AA%E0%B8%B2%E0%B8%82%E0%B8%B2%E0%B8%A7%E0%B8%B4%E0%B8%8A%E0%B8%B2%E0%B9%80%E0%B8%97%E0%B8%84%E0%B9%82%E0%B8%99%E0%B9%82%E0%B8%A5%E0%B8%A2%E0%B8%B5%E0%B8%94%E0%B8%B4%E0%B8%88%E0%B8%B4%E0%B8%97/",
            "https://ead.barueri.sp.gov.br/ola-mundo/",
            "https://drc.uog.edu.et/introducing-dr-deniz-zeynep-2/",
            "https://drc.uog.edu.et/admin-earns-scholarship/",
            "https://cybersecurity.illinois.edu/privacy-everywhere-2023-conference-session-highlights/",
            "https://colegiosanagustin.edu.ve/archivos/1",
            "https://coi.uog.edu.et/our-classes/",
            "https://coi.uog.edu.et/introducing-dr-deniz-zeynep-2/",
            "https://cnacs.uog.edu.et/lms-wordpress-plugin/",
            "https://cnacs.uog.edu.et/admin-earns-scholarship/",
            "https://cjps.coou.edu.ng/professor-albert-joint-research-on-mobile-money-in-tanzania-is-highlighted/",
            "https://blogs.oregonstate.edu/cohesivestrategy/2020/04/11/hello-world/",
            "https://blogs.evergreen.edu/ecotourism/2013/11/22/paradise-lost-on-maldives-rubbish-island/",
            "https://blogs.dickinson.edu/outing-club/2014/09/30/1030-outdoor-fun-with-jack-please-comment/",
            "https://blog.uvm.edu/bdonaghe/comments-conversation/",
            "https://blnews.net/2020/06/an-interview-with-the-director-of-you-will-die-in-the-twentieth-there-is-no-censorship-in-sudan-because-there-is-no-cinema/",
            "https://beritaterkini.co.id/2020/09/17/polda-jawa-barat-ungkap-motif-pelaku-penggunting-bendera-merah-putih-di-sumedang/",
            "https://beritaterkini.co.id/2020/07/31/berhasilnya-polri-dalam-menangkap-joko-tjandra-patut-diapresiasi/",
            "https://beritaterkini.co.id/2019/12/29/pengacara-sebut-pelaku-teror-ke-novel-baswedan-hanya-pemain-pengganti/",
            "https://antidroga.interno.gov.it/uffici-dcsa-roma/",
            "https://adsujsr.adsu.edu.ng/article1/",
            "https://adsujsr.adsu.edu.ng/9-2/",
            "http://thphuocvinha.pgdphugiao.edu.vn/truong-th-phuoc-vinh-a-dat-thanh-tich-cao-trong-hoi-thi-gvg-huyen-nam-hoc-2018-2019/",
            "http://sci.oouagoiwoye.edu.ng/2018/05/15/programme-philosophy-and-objectives/",
            "http://paredezlab.biology.washington.edu/news/congratulations-to-kelly-and-bill-for-successfully-defending-their-theses",
            "http://classweb2.putai.ntct.edu.tw/classweb/1010302/2013/03/13/%E6%81%AD%E8%B3%80%EF%BC%81302%E5%85%A8%E6%96%B0%E9%A2%A8%E8%B2%8C/",
            "http://bmes.seas.ucla.edu/blog/bioengineering-faculty-spotlight-dr-aaron-meyer",
            "http://blogs.evergreen.edu/ecotourism/2013/11/22/272/",
            "http://blogs.cae.tntech.edu/jwlangston21/2010/06/25/battery-powered-usb-phone-charger/",
            "http://apps.lonestar.edu/blogs/acordaway/2015/11/19/hello-world/",
            "https://portalbromo.com/hari-ini-tim-khusus-polri-periksa-irjen-ferdy-sambo-sebagai-tersangka/",
            "https://npcnewstv.com/2019-ifbb-st-louis-pro-bikini-overall-winner-jessica-palmer-after-show-interview/",
            "https://wildlifedirect.org/events/global-march-elephants-rhinos-nairobi/",
            "https://morristownbooks.org/session/chris-whipple/",
            "https://thestoriesofchange.com/mhat-manoj-kumar-kerala-mental-health/",
            "https://blogg.ng.se/amydiamondpodden/2019/11/oppet-brev-till-paradise-hotel-produktionen",
            "https://vlevs.com/7-kalimat-inversi-inversion/",
            "https://diy.open.ubc.ca/computer/create-it/annotated-presentations/",
            "https://www.tvwatchers.nl/inschrijven-the-voice-kids/",
            "https://patioscenes.com/what-is-gazebo-screen/",
            "https://collectivedge.com/blog/five-tips-making-first-vlog/",
            "https://www.visitfashions.com/latest-indian-mehndi-designs/",
            "https://www.sulexinternational.com/container-homes-are-dangerous/",
            "https://www.pickthebrain.com/blog/5-reasons-tell-truth/",
            "https://fx7.xbiz.jp/prospect-riron/",
            "https://www.wartmaansoch.com/raja-parikshit-story-in-hindi/",
            "https://www.raadrechtshandhaving.com/nl_NL/foundation-judicial-institutes-st-maarten/",
            "https://whatishannadoing.com/travel/canada/bc-restaurant/golden-ocean-seafood-restaurant-vancouver/",
            "https://www.repeatcrafterme.com/2013/01/crochet-bunny-hat-pattern.html",
            "https://navimumbaihouses.com/blog/news/griha-pravesh-in-2022/",
            "https://www.gympik.com/articles/25-motivational-quotes-for-women/",
            "https://blogs.millersville.edu/drhydro/2012/11/24/saturday/",
            "https://www.bly.com/blog/online-marketing/does-accepting-affiliate-commissions-cheat-your-customer/",
            "https://www.mjs.gov.mg/?attachment_id=11",
            "https://feettothefire.blogs.wesleyan.edu/2009/02/26/olin-library-opening/",
            "https://visavis.com.ar/2021/09/09/un-entrenador-israeli-de-basquet-es-candidato-al-salon-de-la-fama/",
            "https://elfocodiario.com/musica/cepeda-e-india-martinez-nos-regalan-el-acustico-de-mas-que-nada/",
            "https://halfbloodchinese.blog.binusian.org/2009/11/13/379/",
            "https://nagasaki.heteml.net/18jgospel/2018/03/18/%E3%82%AB%E3%83%AA%E3%82%B9/",
            "https://www.health.go.ug/2022/09/22/prevention-of-ebola-2/",
        ]
        nofollow(urls, "nofollow.json")
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
