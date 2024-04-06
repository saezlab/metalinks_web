import streamlit as st
from neo4j_controller import Neo4jController
import pandas as pd
import base64
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json
sys.path.append('..')
# from aux import create_graph
import streamlit.components.v1 as components
import yaml
with open("data/help_texts.yaml", 'r') as stream:
    help_texts = yaml.safe_load(stream)

st.set_page_config(page_title='Metalinks Web App', layout='wide')

logo_image = Image.open("data/metalinks_logo.png")

import io

logo_bytes = io.BytesIO()
logo_image.save(logo_bytes, format="PNG")
logo_base64 = base64.b64encode(logo_bytes.getvalue()).decode()

# Set the favicon
favicon_html = f"""
    <link rel="icon" href="data:image/png;base64,{logo_base64}">
    """

# Render the favicon HTML
st.markdown(favicon_html, unsafe_allow_html=True)

st.sidebar.image(logo_image, use_column_width=True)

n4j = Neo4jController(
    st.secrets["neo4j_uri"],
    st.secrets["neo4j_user"],
    st.secrets["neo4j_password"],
)

help_celloc = help_texts['multiselect_cellloc']
st.sidebar.write("Select your parameters for contextualization")
cellular_locations = st.sidebar.multiselect("Select cellular locations", 
                                            ["Cytoplasm", "Endoplasmic reticulum", "Extracellular", "Golgi apparatus", 
                                            "Lysosome", "Membrane", "Mitochondria", "Nucleus", "Peroxisome"], 
                                            default=["Extracellular"], help=help_celloc
                                              )

help_tissueloc = help_texts['multiselect_tissue']    
tissue_locations = st.sidebar.multiselect('Select tissue locations', ["Adipose Tissue", "Adrenal Cortex", "Adrenal Gland", "Adrenal Medulla", "All Tissues",
                                                                     "Bladder", "Brain", "Epidermis", "Fibroblasts", "Heart", "Intestine", 
                                                                     "Kidney", "Leukocyte", "Lung", "Neuron", "Ovary", "Pancreas", "Placenta",
                                                                      "Platelet", "Prostate", "Skeletal Muscle", "Spleen", "Testis", "Thyroid Gland"],
                                                                      default=["Kidney", "All Tissues"], help=help_tissueloc)

help_biospecloc = help_texts['multiselect_biospec']
biospecimen_locations = st.sidebar.multiselect('Select biospecimen locations', ['Blood', 'Urine', 'Saliva', 'Cerebrospinal Fluid',
                                                                                'Feces', 'Sweat', 'Breast Milk', 'Bile', 'Amniotic Fluid'],
                                                                                default=['Blood'], help=help_biospecloc )

help_pathway = help_texts['multiselect_pathway']
pathways = st.sidebar.multiselect('Select pathways', ['Anderson disease', 'Debrancher glycogenosis', 'Tay-sachs disease',  'X Linked Dominant (CDPX2)', 'aspartate and glutamate metabolism', 'Carnosinemia', 'cblG complementation type', 'Cystathionine beta-synthase deficiency', 'Guanidinoacetate methyltransferase deficiency', 'Leucine and isoleucine degradation', 'serine and threonine metabolism', 'AICA-Ribosiduria', 'Abacavir Action Pathway', 'Acebutolol Action Pathway', 'Acenocoumarol Action Pathway', 'Acetaminophen  Action Pathway', 
                                                        'Acetaminophen Metabolism Pathway', 'Acetylsalicylic Acid Action Pathway', 'Acrivastine H1-Antihistamine Action', 'Activation of PKC through G protein coupled receptor', 'Acute Intermittent Porphyria', 'Adefovir Dipivoxil  Action Pathway', 'Adefovir Dipivoxil Metabolism Pathway', 'Adenine phosphoribosyltransferase deficiency (APRT)', 'Adenosine Deaminase Deficiency', 'Adenylosuccinate Lyase Deficiency', 'Adrenal Hyperplasia Type 3 or Congenital Adrenal Hyperplasia due to 21-hydroxylase Deficiency', 
                                                        'Adrenal Hyperplasia Type 5 or Congenital Adrenal Hyperplasia due to 17 Alpha-hydroxylase Deficiency', 'Adrenoleukodystrophy', 'Alanine', 'Alcaftadine H1-Antihistamine Action', 'Alendronate Action Pathway', 'Alfentanil Action Pathway', 'Alimemazine H1-Antihistamine Action', 'Alkaptonuria', 'Alprenolol Action Pathway', 'Alteplase Action Pathway', 'Alvimopan Action Pathway', 'Amikacin Action Pathway', 'Amiloride Action Pathway', 'Amino Sugar Metabolism', 'Aminocaproic Acid Action Pathway', 'Amiodarone Action Pathway', 
                                                        'Amlodipine Action Pathway', 'Androgen and Estrogen Metabolism', 'Androstenedione Metabolism', 'Angiotensin Metabolism', 'Anileridine Action Pathway', 'Anistreplase Action Pathway', 'Antazoline H1-Antihistamine Action', 'Antipyrine Action Pathway', 'Antrafenine Action Pathway', 'Apparent mineralocorticoid excess syndrome', 'Aprotinin Action Pathway', 'Arachidonic Acid Metabolism', 'Arbekacin Action Pathway', 'Arbutamine Action Pathway', 'Ardeparin Action Pathway', 'Argatroban Action Pathway', 'Arginine and proline metabolism', 
                                                        'Arginine: Glycine Amidinotransferase Deficiency (AGAT Deficiency)', 'Argininemia', 'Argininosuccinic Aciduria', 'Aromatase deficiency', 'Aromatic L-Aminoacid Decarboxylase Deficiency', 'Artemether Metabolism Pathway', 'Aspartate Metabolism', 'Astemizole H1-Antihistamine Action', 'Atenolol Action Pathway', 'Atorvastatin Action Pathway', 'Azatadine H1-Antihistamine Action', 'Azathioprine Action Pathway', 'Azathioprine Metabolism Pathway', 'Azelastine H1-Antihistamine Action', 'Azithromycin Action Pathway', 'Bafetinib Inhibition of BCR-ABL', 
                                                        'Bamipine H1-Antihistamine Action', 'Benazepril Action Pathway', 'Benazepril Metabolism Pathway', 'Bendroflumethiazide Action Pathway', 'Benzocaine Action Pathway', 'Bepotastine H1-Antihistamine Action', 'Beta Ureidopropionase Deficiency', 'Beta-Ketothiolase Deficiency', 'Beta-mercaptolactate-cysteine disulfiduria', 'Betahistine H1-Antihistamine Action', 'Betaxolol Action Pathway', 'Betazole Action Pathway', 'Bevantolol Action Pathway', 'Bilastine H1-Antihistamine Action', 'Biosynthesis of unsaturated fatty acids', 'Biotin Metabolism', 'Biotinidase Deficiency', 
                                                        'Bisoprolol Action Pathway', 'Bivalirudin Action Pathway', 'Blue diaper syndrome', 'Bopindolol Action Pathway', 'Bosutinib Inhibition of BCR-ABL', 'Bromfenac Action Pathway', 'Bromodiphenhydramine H1-Antihistamine Action', 'Brompheniramine H1-Antihistamine Action', 'Buclizine H1-Antihistamine Action', 'Bumetanide Action Pathway', 'Bupivacaine Action Pathway', 'Bupranolol Action Pathway', 'Buprenorphine Action Pathway', 'Butyrate Metabolism', 'CHILD Syndrome', 'Caffeine Metabolism', 'Canavan Disease', 'Candesartan Action Pathway', 'Capecitabine Action Pathway',
                                                         'Capecitabine Metabolism Pathway', 'Captopril Action Pathway', 'Carbamazepine Metabolism Pathway', 'Carbamoyl Phosphate Synthetase Deficiency', 'Carbinoxamine H1-Antihistamine Action', 'Cardiolipin Biosynthesis', 'Cardiolipin Biosynthesis (Barth Syndrome)', 'Carfentanil Action Pathway', 'Carnitine Synthesis', 'Carnitine palmitoyl transferase deficiency (I)', 'Carnitine palmitoyl transferase deficiency (II)', 'Carnitine-acylcarnitine translocase deficiency', 'Carnosinuria', 'Carprofen Action Pathway', 'Carteolol Action Pathway', 'Carvedilol Action Pathway', 'Celecoxib Action Pathway', 'Celecoxib Metabolism Pathway', 'Cerebrotendinous Xanthomatosis (CTX)', 'Cerivastatin Action Pathway', 'Cetirizine H1-Antihistamine Action', 'Chloramphenicol Action Pathway', 'Chlorcyclizine H1-Antihistamine Action', 'Chloroprocaine Action Pathway', 'Chloropyramine H1-Antihistamine Action', 
                                                         'Chlorothiazide Action Pathway', 'Chlorphenamine H1-Antihistamine Action', 'Chlorphenoxamine H1-Antihistamine Action', 'Chlorthalidone Action Pathway', 'Cholesteryl ester storage disease', 'Chondrodysplasia Punctata II', 'Cilazapril Action Pathway', 'Cilazapril Metabolism Pathway', 'Cilostazol Action Pathway', 'Cimetidine Action Pathway', 'Cimetidine Metabolism Pathway', 'Cinnarizine H1-Antihistamine Action', 'Citalopram Action Pathway', 'Citalopram Metabolism Pathway', 'Citric Acid Cycle', 'Citrullinemia Type I', 'Clarithromycin Action Pathway', 'Clemastine H1-Antihistamine Action', 'Clindamycin Action Pathway', 'Clocinizine H1-Antihistamine Action', 'Clomipramine Metabolism Pathway', 'Clomocycline Action Pathway', 'Clopidogrel Action Pathway', 'Clopidogrel Metabolism Pathway', 'Coagulation ', 'Cocaine Action Pathway', 'Codeine Action Pathway', 'Codeine Metabolism Pathway', 'Congenital Bile Acid Synthesis Defect Type II', 'Congenital Bile Acid Synthesis Defect Type III', 
                                                         'Congenital Erythropoietic Porphyria (CEP) or Gunther Disease', 'Congenital Lipoid Adrenal Hyperplasia (CLAH) or Lipoid CAH', 'Congenital disorder of glycosylation CDG-IId', 'Congenital lactic acidosis', 'Corticosterone methyl oxidase I deficiency (CMO I)', 'Corticosterone methyl oxidase II deficiency - CMO II', 'Corticotropin Activation of Cortisol Production', 'Creatine deficiency', 'Cyclizine H1-Antihistamine Action', 'Cyclophosphamide Action Pathway', 'Cyclophosphamide Metabolism Pathway', 'Cyclothiazide Action Pathway', 'Cyproheptadine H1-Antihistamine Action', 'Cystathionine Beta-Synthase Deficiency', 'Cysteine Metabolism', 'Cystinosis', 'Cystinuria', 'D-Arginine and D-Ornithine Metabolism', 'D-glyceric acidura', 'DNA Replication Fork', 'Dasatinib Inhibition of BCR-ABL', 'De Novo Triacylglycerol Biosynthesis', 'Degradation of Superoxides', 'Delavirdine Action Pathway', 'Demeclocycline Action Pathway', 'Deptropine H1-Antihistamine Action', 'Desipramine Action Pathway', 'Desipramine Metabolism Pathway',
                                                        'Desloratadine H1-Antihistamine Action', 'Desmosterolosis', 'Dexbrompheniramine H1-Antihistamine Action', 'Dexchlorpheniramine H1-Antihistamine Action', 'Dezocine Action Pathway', 'Dibucaine Action Pathway', 'Diclofenac Action Pathway', 'Dicoumarol Action Pathway', 'Dicumarol Action Pathway', 'Didanosine Action Pathway', 'Diflunisal Action Pathway', 'Dihydromorphine Action Pathway', 'Dihydropyrimidinase Deficiency', 'Dihydropyrimidine Dehydrogenase Deficiency (DHPD)', 'Diltiazem Action Pathway', 'Dimethylglycine Dehydrogenase Deficiency', 'Dimethylthiambutene Action Pathway', 'Dimetindene H1-Antihistamine Action', 'Diphenhydramine H1-Antihistamine Action', 'Diphenoxylate Action Pathway', 'Diphenylpyraline H1-Antihistamine Action', 'Dipyridamole (Antiplatelet) Action Pathway', 'Disopyramide Action Pathway', 'Disulfiram Action Pathway', 'Dobutamine Action Pathway', 'Docetaxel Action Pathway', 'Dopa-responsive dystonia', 'Dopamine Activation of Neurological Reward System', 'Dopamine beta-hydroxylase deficiency', 'Doxepin H1-Antihistamine Action',
                                                        'Doxepin Metabolism Pathway', 'Doxorubicin Metabolism Pathway', 'Doxycycline Action Pathway', 'Doxylamine H1-Antihistamine Action', 'Ebastine H1-Antihistamine Action', 'Efavirenz Action Pathway', 'Embramine H1-Antihistamine Action', 'Emedastine H1-Antihistamine Action', 'Emtricitabine Action Pathway', 'Enalapril Action Pathway', 'Enalapril Metabolism Pathway', 'Enoxaparin Action Pathway', 'Epinastine H1-Antihistamine Action', 'Epinephrine Action Pathway', 'Eplerenone Action Pathway', 'Eprosartan Action Pathway', 'Erlotinib Action Pathway', 'Erythromycin Action Pathway', 'Escitalopram Action Pathway', 'Esmolol Action Pathway', 'Esomeprazole Action Pathway', 'Esomeprazole Metabolism Pathway', 'Estrone Metabolism', 'Ethacrynic Acid Action Pathway', 'Ethanol Degradation', 'Ethylmalonic Encephalopathy', 'Ethylmorphine Action Pathway', 'Etodolac Action Pathway', 'Etoposide Action Pathway', 'Etoposide Metabolism Pathway', 'Etoricoxib Action Pathway', 'Excitatory Neural Signalling Through 5-HTR 4 and Serotonin', 'Excitatory Neural Signalling Through 5-HTR 6 and Serotonin', 'Excitatory Neural Signalling Through 5-HTR 7 and Serotonin', 'Fabry disease', 'Familial Hypercholanemia (FHCA)', 'Familial lipoprotein lipase deficiency', 
                                                        'Famotidine Action Pathway', 'Fanconi-bickel syndrome', 'Fatty Acid Biosynthesis', 'Fatty Acid Elongation In Mitochondria', 'Fatty acid Metabolism', 'Fc Epsilon Receptor I Signaling in Mast Cells', 'Felbamate Metabolism Pathway', 'Felodipine Action Pathway', 'Felodipine Metabolism Pathway', 'Fenethazine H1-Antihistamine Action', 'Fenoprofen Action Pathway', 'Fentanyl Action Pathway', 'Fexofenadine H1-Antihistamine Action', 'Flecainide Action Pathway', 'Flunarizine H1-Antihistamine Action', 'Fluorouracil Action Pathway', 'Fluorouracil Metabolism Pathway', 'Fluoxetine Action Pathway', 'Fluoxetine Metabolism Pathway', 'Flurbiprofen Action Pathway', 'Fluvastatin Action Pathway', 'Folate malabsorption', 'Fondaparinux Action Pathway', 'Forasartan Action Pathway', 'Fosinopril Action Pathway', 'Fosinopril Metabolism Pathway', 'Fosphenytoin (Antiarrhythmic) Action Pathway', 'Fosphenytoin (Antiarrhythmic) Metabolism Pathway', 'Fructose and mannose metabolism', 'Fructose intolerance', 'Fructose-1', 'Fructosuria', 'Fumarase deficiency', 'Furosemide Action Pathway', 'G(M2)-Gangliosidosis: Variant B', 'GABA-Transaminase Deficiency', 'GLUT-1 deficiency syndrome', 'Galactose Metabolism', 'Galactosemia', 'Galactosemia II (GALK)', 'Galactosemia III',
                                                        'Gamma-Glutamyltransferase Deficiency', 'Gamma-cystathionase deficiency (CTH)', 'Gamma-glutamyl-transpeptidase deficiency', 'Gastric Acid Production', 'Gaucher Disease', 'Gefitinib Action Pathway', 'Gemcitabine Action Pathway', 'Gemcitabine Metabolism Pathway', 'Gentamicin Action Pathway', 'Glibenclamide Action Pathway', 'Gliclazide Action Pathway', 'Globoid Cell Leukodystrophy', 'Glucose Transporter Defect (SGLT2)', 'Glucose-6-phosphate dehydrogenase deficiency', 'Glucose-Alanine Cycle', 'Glutamate Metabolism', 'Glutaminolysis and Cancer', 'Glutaric Aciduria Type I', 'Glutathione Synthetase Deficiency', 'Glutathione metabolism', 'Glycerol Kinase Deficiency', 'Glycerol Phosphate Shuttle', 'Glycerolipid Metabolism', 'Glycine', 'Glycine N-methyltransferase Deficiency', 'Glycogen Storage Disease Type 1A (GSD1A) or Von Gierke Disease', 'Glycogen synthetase deficiency', 'Glycogenosis', 'Glycolysis / Gluconeogenesis', 'Gout or Kelley-Seegmiller Syndrome', 'Guanidinoacetate Methyltransferase Deficiency (GAMT Deficiency)', 'Hartnup Disorder', 'Hawkinsinuria', 'Heparin Action Pathway', 'Hereditary Coproporphyria (HCP)', 'Heroin Action Pathway', 'Heroin Metabolism Pathway', 'Histamine H1 Receptor Activation', 
                                                        'Histapyrrodine H1-Antihistamine Action', 'Histidine metabolism', 'Histidinemia', 'Homocarnosinosis', 'Homochlorcyclizine H1-Antihistamine Action', 'Homocysteine Degradation', 'Homocystinuria', 'Homocystinuria-megaloblastic anemia due to defect in cobalamin metabolism', 'Hydrochlorothiazide Action Pathway', 'Hydrocodone Action Pathway', 'Hydroflumethiazide Action Pathway', 'Hydromorphone Action Pathway', 'Hydroxyethylpromethazine H1-Antihistamine Action', 'Hydroxyzine H1-Antihistamine Action', 'Hyper-IgD syndrome', 'Hypercholesterolemia', 'Hyperglycinemia', 'Hyperinsulinism-Hyperammonemia Syndrome', 'Hyperlysinemia I', 'Hyperlysinemia II or Saccharopinuria', 'Hypermethioninemia', 'Hyperornithinemia with gyrate atrophy (HOGA)', 'Hyperornithinemia-hyperammonemia-homocitrullinuria [HHH-syndrome]', 'Hyperphenylalaniemia due to guanosine triphosphate cyclohydrolase deficiency', 'Hyperphenylalaninemia due to 6-pyruvoyltetrahydropterin synthase deficiency (ptps)', 'Hyperphenylalaninemia due to dhpr-deficiency', 'Hyperprolinemia Type I', 'Hyperprolinemia Type II', 'Hypoacetylaspartia', 'Hypophosphatasia', 'Ibandronate Action Pathway', 'Ibuprofen Action Pathway', 'Ibuprofen Metabolism Pathway', 
                                                        'Ibutilide Action Pathway', 'Ifosfamide Action Pathway', 'Ifosfamide Metabolism Pathway', 'Imatinib Inhibition of BCR-ABL', 'Iminoglycinuria', 'Imipramine Action Pathway', 'Imipramine Metabolism Pathway', 'Indapamide Action Pathway', 'Indomethacin Action Pathway', 'Inositol Phosphate Metabolism', 'Inositol phosphate metabolism', 'Insulin Signalling', 'Intracellular Signalling Through Adenosine Receptor A2a and Adenosine', 'Intracellular Signalling Through Adenosine Receptor A2b and Adenosine', 'Intracellular Signalling Through FSH Receptor and Follicle Stimulating Hormone', 'Intracellular Signalling Through Histamine H2 Receptor and Histamine', 'Intracellular Signalling Through LHCGR Receptor and Luteinizing Hormone/Choriogonadotropin', 'Intracellular Signalling Through PGD2 receptor and Prostaglandin D2', 'Intracellular Signalling Through Prostacyclin Receptor and Prostacyclin', 'Irbesartan Action Pathway', 'Irinotecan Action Pathway', 'Irinotecan Metabolism Pathway', 'Isobutyryl-coa dehydrogenase deficiency', 'Isoprenaline Action Pathway', 'Isothipendyl H1-Antihistamine Action', 'Isovaleric Aciduria', 'Isovaleric acidemia', 'Isradipine Action Pathway', 'Josamycin Action Pathway', 
                                                        'Joubert syndrome', 'Kanamycin Action Pathway', 'Ketobemidone  Action Pathway', 'Ketone Body Metabolism', 'Ketoprofen Action Pathway', 'Ketorolac Action Pathway', 'Ketotifen H1-Antihistamine Action', 'Kidney Function', 'Krabbe disease', 'L-arginine:glycine amidinotransferase deficiency', 'Labetalol Action Pathway', 'Lactic Acidemia', 'Lactose Degradation', 'Lactose Intolerance', 'Lactose Synthesis', 'Lafutidine H2-Antihistamine Action', 'Lamivudine  Action Pathway', 'Lamivudine Metabolism Pathway', 'Lansoprazole Action Pathway', 'Lansoprazole Metabolism Pathway', 'Latrepirdine H1-Antihistamine Action', 'Leigh Syndrome', 'Lepirudin Action Pathway', 'Lesch-Nyhan Syndrome (LNS)', 'Leucine Stimulation on Insulin Signaling', 'Leukotriene C4 Synthesis Deficiency', 'Levallorphan Action Pathway', 'Levobunolol Action Pathway', 'Levobupivacaine Action Pathway', 'Levocabastine H1-Antihistamine Action', 'Levocetirizine H1-Antihistamine Action', 'Levomethadyl Acetate Action Action Pathway', 'Levomethadyl Acetate Metabolism Pathway', 'Levorphanol Action Pathway', 'Lidocaine (Antiarrhythmic) Action Pathway', 'Lidocaine (Local Anaesthetic) Action Pathway', 'Lidocaine (Local Anaesthetic) Metabolism Pathway', 
                                                        'Lincomycin Action Pathway', 'Lisinopril Action Pathway', 'Long chain acyl-CoA dehydrogenase deficiency (LCAD)', 'Long-chain-3-hydroxyacyl-coa dehydrogenase deficiency (LCHAD)', 'Loratadine H1-Antihistamine Action', 'Lornoxicam Action Pathway', 'Losartan Action Pathway', 'Lovastatin Action Pathway', 'Lumiracoxib Action Pathway', 'Lymecycline Action Pathway', 'Lysine degradation', 'Lysinuric Protein Intolerance', 'Lysinuric protein intolerance (LPI)', 'Lysophosphatidic Acid LPA1 Signalling', 'Lysophosphatidic Acid LPA2 Signalling', 'Lysophosphatidic Acid LPA3 Signalling', 'Lysophosphatidic Acid LPA4 Signalling', 'Lysophosphatidic Acid LPA5 Signalling', 'Lysophosphatidic Acid LPA6 Signalling', 'Lysosomal Acid Lipase Deficiency (Wolman Disease)', 'MNGIE (Mitochondrial Neurogastrointestinal Encephalopathy)', 'Magnesium salicylate Action Pathway', 'Malate-Aspartate Shuttle', 'Malonic Aciduria', 'Malonyl-coa decarboxylase deficiency', 'Maple Syrup Urine Disease', 'Mebhydrolin H1-Antihistamine Action', 'Meclizine H1-Antihistamine Action', 'Medium chain acyl-coa dehydrogenase deficiency (MCAD)', 'Mefenamic Acid Action Pathway', 'Meloxicam Action Pathway', 'Mepivacaine Action Pathway', 'Mepyramine H1-Antihistamine Action', 
                                                        'Mequitazine H1-Antihistamine Action', 'Mercaptopurine Action Pathway', 'Mercaptopurine Metabolism Pathway', 'Metachromatic Leukodystrophy (MLD)', 'Methacycline Action Pathway', 'Methadone Action Pathway', 'Methadone Metabolism Pathway', 'Methadyl Acetate Action Pathway', 'Methapyrilene H1-Antihistamine Action', 'Methdilazine H1-Antihistamine Action', 'Methionine Adenosyltransferase Deficiency', 'Methionine Metabolism', 'Methotrexate Action Pathway', 'Methyclothiazide Action Pathway', 'Methylenetetrahydrofolate Reductase Deficiency (MTHFRD)', 'Methylhistidine Metabolism', 'Methylmalonate Semialdehyde Dehydrogenase Deficiency', 'Methylmalonic Aciduria', 'Methylmalonic Aciduria Due to Cobalamin-Related Disorders', 'Metiamide Action Pathway', 'Metipranolol Action Pathway', 'Metolazone Action Pathway', 'Metoprolol Action Pathway', 'Mevalonic aciduria', 'Mexiletine Action Pathway', 'Minocycline Action Pathway', 'Mirtazapine H1-Antihistamine Action', 'Mitochondrial Beta-Oxidation of Long Chain Saturated Fatty Acids', 'Mitochondrial Beta-Oxidation of Medium Chain Saturated Fatty Acids', 'Mitochondrial Beta-Oxidation of Short Chain Saturated Fatty Acids', 'Mitochondrial DNA depletion syndrome', 'Mitochondrial complex II deficiency', 'Mizolastine H1-Antihistamine Action', 'Moexipril Action Pathway', 
                                                        'Moexipril Metabolism Pathway', 'Molybdenum Cofactor Deficiency', 'Monoamine oxidase-a deficiency (MAO-A)', 'Morphine Action Pathway', 'Morphine Metabolism Pathway', 'Mucopolysaccharidosis VI. Sly syndrome', 'Multiple carboxylase deficiency', 'Muscle/Heart Contraction', 'Mycophenolic Acid Metabolism Pathway', 'Myoadenylate deaminase deficiency', 'Nabumetone Action Pathway', 'Nadolol Action Pathway', 'Nalbuphine Action Pathway', 'Naloxone Action Pathway', 'Naltrexone Action Pathway', 'Naproxen Action Pathway', 'Nateglinide Action Pathway', 'Nebivolol Action Pathway', 'Neomycin Action Pathway', 'Nepafenac Action Pathway', 'Netilmicin Action Pathway', 'Nevirapine  Action Pathway', 'Nevirapine Metabolism Pathway', 'Nicotinate and nicotinamide metabolism', 'Nicotine Action Pathway', 'Nicotine Metabolism Pathway', 'Nifedipine Action Pathway', 'Nilotinib Inhibition of BCR-ABL', 'Nimodipine Action Pathway', 'Nisoldipine Action Pathway', 'Nitrendipine Action Pathway', 'Nitrogen metabolism', 'Nizatidine Action Pathway', 'Non Ketotic Hyperglycinemia', 'Nucleotide Sugars Metabolism', 'Olmesartan Action Pathway', 'Olopatadine H1-Antihistamine Action', 'Omeprazole Action Pathway', 'Omeprazole Metabolism Pathway', 'One carbon pool by folate', 'Ornithine Aminotransferase Deficiency (OAT Deficiency)', 
                                                        'Ornithine Transcarbamylase Deficiency (OTC Deficiency)', 'Orphenadrine H1-Antihistamine Action', 'Oxaprozin Action Pathway', 'Oxatomide H1-Antihistamine Action', 'Oxidation of Branched Chain Fatty Acids', 'Oxidative phosphorylation', 'Oxomemazine H1-Antihistamine Action', 'Oxprenolol Action Pathway', 'Oxybuprocaine Action Pathway', 'Oxycodone Action Pathway', 'Oxymorphone Action Pathway', 'Oxytetracycline Action Pathway', 'Paclitaxel Action Pathway', 'Pamidronate Action Pathway', 'Pancreas Function', 'Pantoprazole Action Pathway', 'Pantoprazole Metabolism Pathway', 'Pantothenate and CoA Biosynthesis', 'Paromomycin Action Pathway', 'Penbutolol Action Pathway', 'Pentazocine Action Pathway', 'Perindopril Action Pathway', 'Phenbenzamine H1-Antihistamine Action', 'Phenindamine H1-Antihistamine Action', 'Phenindione Action Pathway', 'Pheniramine H1-Antihistamine Action', 'Phenprocoumon Action Pathway', 'Phenylalanine and Tyrosine Metabolism', 'Phenylalanine metabolism', 'Phenylbutazone Action Pathway', 'Phenylketonuria', 'Phenyltoloxamine H1-Antihistamine Action', 'Phenytoin (Antiarrhythmic) Action Pathway', 'Phosphatidylcholine Biosynthesis', 'Phosphatidylethanolamine Biosynthesis', 'Phosphatidylinositol Phosphate Metabolism', 'Phosphoenolpyruvate carboxykinase deficiency 1 (PEPCK1)', 'Phospholipid Biosynthesis', 'Phytanic Acid Peroxisomal Oxidation', 'Pimethixene H1-Antihistamine Action', 'Pindolol Action Pathway', 'Pirenzepine Action Pathway', 'Piroxicam Action Pathway', 'Plasmalogen Synthesis', 'Polythiazide Action Pathway', 'Ponatinib Inhibition of BCR-ABL', 'Porphyria Variegata (PV)', 'Porphyrin Metabolism', 'Practolol Action Pathway', 'Pravastatin Action Pathway', 'Prednisolone Action Pathway', 'Prednisolone Metabolism Pathway', 'Prednisone Action Pathway', 'Prednisone Metabolism Pathway', 'Prilocaine Action Pathway', 'Primary Hyperoxaluria Type I', 
                                                        'Primary bile acid biosynthesis', 'Primary hyperoxaluria II', 'Procainamide (Antiarrhythmic) Action Pathway', 'Procaine Action Pathway', 'Prolidase Deficiency (PD)', 'Prolinemia Type II', 'Promethazine H1-Antihistamine Action', 'Propanoate metabolism', 'Proparacaine Action Pathway', 'Propiomazine H1-Antihistamine Action', 'Propionic Acidemia', 'Propoxyphene Action Pathway', 'Propranolol Action Pathway', 'Pterine Biosynthesis', 'Purine Nucleoside Phosphorylase Deficiency', 'Purine metabolism', 'Pyridoxine dependency with seizures', 'Pyrimidine metabolism', 'Pyrrobutamine H1-Antihistamine Action', 'Pyruvaldehyde Degradation', 'Pyruvate Carboxylase Deficiency', 'Pyruvate Decarboxylase E1 Component Deficiency (PDHE1 Deficiency)', 'Pyruvate Dehydrogenase Complex Deficiency', 'Pyruvate dehydrogenase deficiency (E2)', 'Pyruvate dehydrogenase deficiency (E3)', 'Pyruvate kinase deficiency', 'Pyruvate metabolism', 
                                                        'Quetiapine H1-Antihistamine Action', 'Quifenadine H1-Antihistamine Action', 'Quinapril Action Pathway', 'Quinapril Metabolism Pathway', 'Quinethazone Action Pathway', 'Quinidine Action Pathway', 'Rabeprazole Action Pathway', 'Rabeprazole Metabolism Pathway', 'Ramipril Action Pathway', 'Ramipril Metabolism Pathway', 'Ranitidine Action Pathway', 'Refsum Disease', 'Remifentanil Action Pathway', 'Repaglinide Action Pathway', 'Rescinnamine Action Pathway', 'Reteplase Action Pathway', 'Retinol Metabolism', 'Riboflavin Metabolism', 'Ribose-5-phosphate isomerase deficiency', 'Rilpivirine Action Pathway', 'Risedronate Action Pathway', 'Rofecoxib Action Pathway', 'Rolitetracycline Action Pathway', 'Ropivacaine Action Pathway', 'Rosiglitazone Metabolism Pathway', 'Rosuvastatin Action Pathway', 'Roxatidine acetate Action Pathway', 'Roxithromycin Action Pathway', 'Rupatadine H1-Antihistamine Action', 'S-Adenosylhomocysteine (SAH) Hydrolase Deficiency', 'Saccharopinuria/Hyperlysinemia II', 'Salicylate-sodium Action Pathway', 'Salicylic Acid Action Pathway', 'Salla Disease/Infantile Sialic Acid Storage Disease', 'Salsalate Action Pathway', 'Sarcosine Oncometabolite Pathway ', 'Sarcosinemia', 'Segawa syndrome', 'Selenocompound metabolism', 'Sepiapterin reductase deficiency', 'Short Chain Acyl CoA Dehydrogenase Deficiency (SCAD Deficiency)', 'Short-chain 3-hydroxyacyl-CoA dehydrogenase deficiency (SCHAD)', 'Sialuria or French Type Sialuria', 'Simvastatin Action Pathway', 'Smith-Lemli-Opitz Syndrome (SLOS)', 'Sorafenib Metabolism Pathway', 'Sotalol Action Pathway', 'Spectinomycin Action Pathway', 'Spermidine and Spermine Biosynthesis', 'Spirapril Action Pathway', 'Spirapril Metabolism Pathway', 'Spironolactone Action Pathway', 'Starch and Sucrose Metabolism', 'Starch and sucrose metabolism', 'Stavudine Action Pathway', 'Steroid Biosynthesis', 'Steroidogenesis', 
                                                        'Streptokinase Action Pathway', 'Streptomycin Action Pathway', 'Succinic semialdehyde dehydrogenase deficiency', 'Succinyl CoA: 3-ketoacid CoA transferase deficiency', 'Sucrase-isomaltase deficiency', 'Sufentanil Action Pathway', 'Sulfite oxidase deficiency', 'Sulfur metabolism', 'Sulindac Action Pathway', 'Suprofen Action Pathway', 'Talastine H1-Antihistamine Action', 'Tamoxifen Action Pathway', 'Tamoxifen Metabolism Pathway', 'Taurine and Hypotaurine Metabolism', 'Tay-Sachs Disease', 'Telithromycin Action Pathway', 'Telmisartan Action Pathway', 'Temelastine H1-Antihistamine Action', 'Temocapril Action Pathway', 'Temocapril Metabolism Pathway', 'Tenecteplase Action Pathway', 'Teniposide Action Pathway', 'Teniposide Metabolism Pathway', 'Tenofovir  Action Pathway', 'Tenofovir Metabolism Pathway', 'Tenoxicam Action Pathway', 'Terfenadine H1-Antihistamine Action', 'Tetracycline Action Pathway', 'The Oncogenic Action of Fumarate', 'The Oncogenic Action of Succinate', 'The oncogenic action of 2-hydroxyglutarate', 'The oncogenic action of D-2-hydroxyglutarate in  Hydroxygluaricaciduria ', 'The oncogenic action of L-2-hydroxyglutarate in  Hydroxygluaricaciduria', 'Thenalidine H1-Antihistamine Action', 'Thenyldiamine H1-Antihistamine Action', 'Thiamine Metabolism', 'Thiazinamium H1-Antihistamine Action', 'Thioguanine Action Pathway', 'Thioguanine Metabolism Pathway', 'Thonzylamine H1-Antihistamine Action', 
                                                        'Threonine and 2-Oxobutanoate Degradation', 'Thyroid hormone synthesis', 'Tiaprofenic Acid Action Pathway', 'Ticlopidine Action Pathway', 'Ticlopidine Metabolism Pathway', 'Tigecycline Action Pathway', 'Timolol Action Pathway', 'Tirofiban Action Pathway', 'Tobramycin Action Pathway', 'Tocainide Action Pathway', 'Tolmetin Action Pathway', 'Tolpropamine H1-Antihistamine Action', 'Torsemide Action Pathway', 'Tramadol Action Action Pathway', 
                                                        'Tramadol Metabolism Pathway', 'Trandolapril Action Pathway', 'Trandolapril Metabolism Pathway', 'Tranexamic Acid Action Pathway', 'Transaldolase deficiency', 'Transcription/Translation', 'Transfer of Acetyl Groups into Mitochondria', 'Trehalose Degradation', 'Triamterene Action Pathway', 'Trichlormethiazide Action Pathway', 'Trifunctional protein deficiency', 'Triosephosphate isomerase', 'Tripelennamine H1-Antihistamine Action', 'Triprolidine H1-Antihistamine Action', 'Trisalicylate-choline Action Pathway', 'Tritoqualine H1-Antihistamine Action', 'Troleandomycin Action Pathway', 'Tryptophan metabolism', 'Tyrosine hydroxylase deficiency', 'Tyrosine metabolism', 'Tyrosinemia', 'Tyrosinemia Type 2 (or Richner-Hanhart syndrome)', 
                                                        'Tyrosinemia Type 3 (TYRO3)', 'Tyrosinemia Type I', 'UMP Synthase Deficiency (Orotic Aciduria)', 'Ubiquinone Biosynthesis', 'Urea Cycle', 'Ureidopropionase Deficiency', 'Urokinase Action Pathway', 'Valdecoxib Action Pathway', 'Valine', 'Valproic Acid Metabolism Pathway', 'Valsartan Action Pathway', 'Vasopressin Regulation of Water Homeostasis', 'Venlafaxine Metabolism Pathway', 'Verapamil Action Pathway', 'Very-long-chain acyl coa dehydrogenase deficiency (VLCAD)', 'Vinblastine Action Pathway', 'Vincristine Action Pathway', 'Vindesine Action Pathway', 'Vinorelbine Action Pathway', 'Vitamin A Deficiency', 'Vitamin B6 Metabolism', 'Vitamin K Metabolism', 'Warburg Effect', 'Warfarin Action Pathway', 'Wolman disease', 'Xanthine Dehydrogenase Deficiency (Xanthinuria)', 'Xanthinuria type I', 'Xanthinuria type II', 'Ximelagatran Action Pathway', 'Zalcitabine Action Pathway', 'Zellweger Syndrome', 'Zidovudine Action Pathway', 'Zoledronate Action Pathway', 'alpha-Linolenic acid metabolism', 'beta-Alanine metabolism', 'pentose phosphate pathway'],
                                                    default=None, help=help_pathway)

help_disease = help_texts['multiselect_disease']
diseases = st.sidebar.multiselect('Select diseases', ['L-2-hydroxyglutaric aciduria', 'Mental Retardation', 'Onychodystrophy', 'Osteodystrophy', 'Polyendocrinopathy', 'Sensorineural deafness', ' subacute necrotizing encephalopathy', '11-beta-Hydroxylase deficiency', '2-Aminoadipic aciduria', '2-Ketoadipic acidemia', '2-Ketoglutarate dehydrogenase complex deficiency', '2-Methyl-3-hydroxybutyryl-CoA dehydrogenase deficiency', '21-Hydroxylase deficiency', '3-Hydroxy-3-Methylglutaryl-CoA Synthase Deficiency', '3-Hydroxy-3-methylglutaryl-CoA lyase deficiency', '3-Hydroxyacyl-CoA dehydrogenase deficiency', '3-Hydroxydicarboxylic aciduria',
                                                     '3-Hydroxyisobutyric acid dehydrogenase deficiency', '3-Hydroxyisobutyric aciduria', '3-Hydroxyisobutyryl-coa hydrolase deficiency', '3-Methyl-crotonyl-glycinuria', '3-Methylglutaconic Aciduria type IV', '3-Methylglutaconic Aciduria type IX', '3-Methylglutaconic Aciduria type V', '3-Methylglutaconic Aciduria type VI', '3-Methylglutaconic aciduria type I', '3-Methylglutaconic aciduria type VII', '3-Phosphoglycerate dehydrogenase deficiency', '3-methylglutaconic aciduria type II', '4-dienoyl-CoA reductase deficiency', '5-oxoprolinase deficiency', '6-Pyruvoyltetrahydropterin synthase deficiency', 
                                                     '6-diphosphatase deficiency', 'ACTH deficiency', 'AIDS', 'ATIC deficiency', 'Abetalipoproteinemia', 'Aceruloplasminemia', 'Acrodermatitis enteropathica', 'Acute Infantile Liver Failure', 'Acute Lymphoblastic Leukemia', 'Acute intermittent porphyria', 'Acute liver disease', 'Acute liver failure', 'Acute myelogenous leukemia', 'Acute promyelocytic leukemia', 'Acute seizures', "Addison's Disease", 'Adenosine deaminase deficiency', 'Adenosine kinase deficiency', 'Adenylosuccinate lyase deficiency', 'Adrenal hyperplasia', 'Adrenal hypoplasia', 'Adrenal insufficiency', 'Adrenoleukodystrophy', 'Adrenomyeloneuropathy', 
                                                     'Alcoholism', 'Aldehyde dehydrogenase deficiency', 'Aldosteronism', 'Alkaptonuria', 'Alpha-1-antitrypsin deficiency', 'Alpha-Methylacyl-CoA racemase deficiency', 'Alpha-aminoadipic aciduria', 'Alpha-aminoadipic and alpha-ketoadipic aciduria', "Alzheimer's disease", 'Aminoacylase I deficiency', 'Amish lethal microcephaly', 'Amyotrophic lateral sclerosis', 'Anemia', 'Anephric patients', 'Angina', 'Anorexia nervosa', 'Anoxia', 'Antley-Bixler syndrome with genital anomalies and disordered steroidogenesis', 'Apparent mineralocorticoid excess', 'Appendicitis', 'Argininemia', 'Argininosuccinic aciduria', 
                                                     'Argininosuccinyl-CoA lyase deficiency', 'Aromatase deficiency', 'Aromatic L-amino acid decarboxylase deficiency', 'Aseptic meningitis', 'Aspartylglucosaminuria', 'Asthma', 'Athyreosis', 'Atrophic gastritis', 'Attachment loss', 'Autism', 'Autosomal  dominant polycystic kidney disease', 'Bacterial infections', 'Bacterial meningitis', 'Bartter Syndrome', 'Beckwith-Wiedemann Syndrome', 'Benign gynecological diseases', 'Benign prostatic hyperplasia', 'Benzene exposure', 'Beta-ketothiolase deficiency', 'Beta-mercaptolactate-cysteine Disulfiduria', 'Beta-thalassemia', 'Beta-ureidopropionase deficiency', 
                                                     'Bile Acid Synthesis Defect', 'Biliary atresia', 'Biotinidase deficiency', 'Bipolar disorder', 'Bladder infections', 'Brain tumors', 'Branched-chain Keto Acid Dehydrogenase Kinase Deficiency', 'Breast cancer', 'Brown-Vialetto-Van Laere Syndrome 1', 'Brunner Syndrome', 'Bulimia nervosa', 'CNS infections', 'CNS tumors', 'Cachexia', 'Cadmium exposure', 'Canavan disease', 'Cancer with metastatic bone disease', 'Carbamoyl Phosphate Synthetase Deficiency', 'Cardiac arrest', 'Cardiopulmonary bypass', 'Cardiopulmonary resuscitation', 'Carnitine palmitoyltransferase I deficiency', 'Carnitine transporter defect; primary systemic carnitine deficiency', 
                                                     'Carnitine-acylcarnitine translocase deficiency', 'Carnosinuria', 'Celiac disease', 'Cerebral creatine deficiency syndrome 1', 'Cerebral creatine deficiency syndrome 2', 'Cerebral creatine deficiency syndrome 3', 'Cerebral folate transport deficiency', 'Cerebral infarction', 'Cerebral vasospasm', 'Cerebrocortical degeneration', 'Cerebrotendinous xanthomatosis', 'Cervical cancer', 'Cervical myelopathy', 'Cholangiocarcinoma', 'Choledochal cysts', 'Cholelithiasis', 'Cholestasis', 'Cholesteryl ester storage disease', 'Chondrodysplasia punctata', 'Chronic active hepatitis', 'Chronic kidney disease', 'Chronic pancreatitis',
                                                      'Chronic progressive external ophthalmoplegia and Kearns-Sayre syndrome', 'Chronic renal failure', 'Cirrhosis', 'Citrullinemia type I', 'Citrullinemia type II', 'Clostridium difficile infection', 'Cobalamin A disease', 'Cobalamin F disease (cblF)', 'Cobalamin malabsorption', 'Coenzyme Q10 deficiency', 'Cognitive disorders', 'Colorectal cancer', 'Combined malonic and methylmalonic aciduria', 'Combined oxidative phosphorylation deficiency 10', 'Combined oxidative phosphorylation deficiency 11', 'Combined oxidative phosphorylation deficiency 12', 'Combined oxidative phosphorylation deficiency 14', 'Congenital Adrenal Hyperplasia',
                                                       'Congenital cataracts', 'Congenital chloride diarrhea', 'Congenital secretory diarrhea', 'Congestive heart failure', 'Continuous ambulatory peritoneal dialysis', 'Convulsion', 'Coronary artery disease', 'Coronary heart disease', 'Cortical myoclonus', 'Corticosterone methyl oxidase I deficiency', 'Cresol poisoning IBS', 'Creutzfeldt-Jakob disease', 'Crigler-Najjar syndrome type I', 'Critical illnesses', "Crohn's disease", "Cushing's Syndrome", 'Cutis laxa', 'Cystathioninuria', 'Cystic fibrosis', 'Cystinosis', 'Cystinuria', 'Cystinylglycinuria', 'Cytochrome C oxidase deficiency', 'D', 'D-2-hydroxyglutaric aciduria', 'D-Bifunctional protein deficiency',
                                                        'D-Glyceric acidemia', 'D-Glyceric acidura', 'D-Lactic Acidosis', 'D-Lactic Acidosis and Short Bowel Syndrome', 'Deafness', 'Degenerative disc disease', 'Dementia', 'Demyelinating polyneuropathy', 'Dengue fever', 'Depersonalization disorder', 'Dermal fibroproliferative disorder', 'Desmosterolosis', 'Diabetes Mellitus', 'Diabetes and Deafness', 'Diabetes mellitus type 1', 'Diabetes mellitus type 2', 'Diarrhoea predominant irritable bowel syndrome', 'Dicarboxylic aminoaciduria', 'Digeorge Syndrome', 'Dihydrolipoamide Dehydrogenase Deficiency', 'Dihydropyrimidinase deficiency', 'Dihydropyrimidine dehydrogenase deficiency', 'Dimethyl sulfide poisoning', 
                                                        'Dimethylglycine Dehydrogenase Deficiency', 'Diverticular disease', 'Donohue Syndrome', 'Dopamine Beta-Hydroxylase Deficiency', 'Dopamine-serotonin Vesicular Transport Defect', 'Duchenne Muscular Dystrophy', 'Early preeclampsia', 'Eczema', 'Encephalitis', 'Endometrial cancer', 'Enteritis', 'Eosinophilic esophagitis', 'Epilepsy', 'Epileptic encephalopathy', 'Erythropoietic protoporphyria', 'Essential hypertension', 'Ethanol intoxication', 'Ethanolaminuria', 'Ethylene glycol poisoning', 'Ethylmalonic encephalopathy', 'Eucalyptol exposure', 'Fabry disease', 'Familial amyotrophic lateral sclerosis', 'Familial mediterranean fever', 'Familial partial lipodystrophy', 
                                                        'Fanconi Bickel syndrome', 'Fanconi syndrome', 'Fatty Acid Oxidation disorder', 'Febrile seizures', 'Fibromyalgia', 'Folate deficiency', 'Formic acid intoxication', "Friedreich's ataxia", 'Frontotemporal dementia', 'Fructose intolerance', 'Fructose-1', 'Fumarase deficiency', 'Functional hypothalamic amenorrhea', 'GRACILE syndrome', 'Gaba-transaminase deficiency', 'Galactose-1-phosphate uridyltransferase deficiency', 'Galactosemia', 'Galactosemia type 1', 'Gallbladder disease', 'Gamma-glutamyl transpeptidase deficiency', 'Gamma-glutamyltransferase deficiency', 'Gestational diabetes', 'Gitelman syndrome', 'Glucagon deficiency', 'Glucocorticoid resistance', 
                                                        'Glucoglycinuria', 'Glucose transporter type 1 deficiency syndrome', 'Glucose-6-phosphate dehydrogenase deficiency', 'Glutamate formiminotransferase deficiency', 'Glutamine deficiency', 'Glutaric acidemia type 2', 'Glutaric aciduria I', 'Glutaric aciduria II', 'Glutaric aciduria type III', 'Glutaryl-CoA dehydrogenase deficiency (GDHD)', 'Glutathione synthetase deficiency', 'Glycerol intolerance syndrome', 'Glycerol kinase deficiency', 'Glycine N-methyltransferase deficiency', 'Glycogen storage disease', 'Glycolic aciduria', 'Gout', 'Growth hormone deficiency', 'Guanosine triphosphate cyclohydrolase deficiency', 'Guillain-Barré syndrome', 'Hartnup disease', 
                                                        'Hawkinsinuria', 'Head injury', 'Headache', 'Heart failure', 'Heat stress', 'Hemochromatosis', 'Hemodialysis', 'Hemolytic uremic syndrome', 'Hepatic and biliary malignancies', 'Hepatic coma', 'Hepatic encephalopathy', 'Hepatitis', 'Hepatobiliary diseases', 'Hepatocellular carcinoma', 'Hereditary coproporphyria', 'Hereditary folate malabsorption', 'Hereditary spastic paraplegia', 'Herpes zoster', 'Hirsutism', 'Histidinemia', 'Homocystinuria', 'Homocystinuria due to defect of N(5', 'Homocystinuria-megaloblastic anemia due to defect in cobalamin metabolism', 'Homozygous sickle cell disease', "Huntington's disease", 'Hydrocephalus', 'Hydrogen sulfide poisoning',
                                                        'Hydroxylysinuria', 'Hydroxyprolinemia', 'Hyper beta-alaninemia', 'Hyperammonemia', 'Hyperargininemia', 'Hypercholesterolemia', 'Hyperdibasic aminoaciduria I', 'Hyperekplexia', 'Hyperglycinemia', 'Hyperinsulinemic hypoglycemia', 'Hyperinsulinism-hyperammonemia syndrome', 'Hyperlipoproteinemia', 'Hyperlysinemia I', 'Hyperlysinuria', 'Hypermanganesemia with dystonia 1', 'Hypermanganesemia with dystonia 2', 'Hypermethioninemia', 'Hyperornithinemia with Gyrate Atrophy', 'Hyperornithinemia-hyperammonemia-homocitrullinuria', 'Hyperoxalemia', 'Hyperphosphatasia', 'Hyperpipecolatemia', 'Hyperprolinemia', 'Hypertension', 'Hyperthyroidism', 'Hypervalinemia', 
                                                        'Hyperzincaemia and hypercalprotectinaemia', 'Hypobetalipoproteinemia', 'Hypoglycemia', 'Hypogonadism', 'Hypomagnesemia 1', 'Hypoparathyroidism-retardation-dysmorphism syndrome', 'Hypophosphatasia', 'Hypophosphatemia', 'Hypothyroidism', 'Hypoxic-ischemic encephalopathy', 'Idiopathic intracranial hypertension', 'Idiopathic oro-facial pain', 'Idiopathic polyneuritis', 'Ileocystoplasty', 'Ileostomy', 'Iminoglycinuria', 'Immunoglobulin A nephropathy', 'Impaired glucose tolerance', 'Infantile Liver Failure Syndrome 2', "Infantile Refsum's disease", 'Inflammatory bowel disease', 'Intestinal failure', 'Intrahepatic biliary hypoplasia',
                                                        'Intraventricular hemorrhage', 'Invasive candidiasis', 'Iron deficiency', 'Irritable bowel syndrome', 'Ischemia', 'Ischemic heart disease', 'Isobutyryl-CoA Dehydrogenase Deficiency', 'Isopropyl alcohol poisoning', 'Isovaleric acidemia', 'Juvenile myoclonic epilepsy', 'Ketoacidosis', 'Ketosis', 'Ketotic hypoglycemia', 'Kidney cancer', 'Kidney disease', 'Kidney transplantation', 'Kynureninase deficiency', 'L-2-Hydroxyglutaric aciduria', 'Lactose Intolerance', 'Late-onset preeclampsia', 'Lathosterolosis', 'Leber Optic Atrophy and Dystonia', 'Lecithin:cholesterol Acyltransferase Deficiency', 'Leigh Syndrome', "Leigh's syndrome", 
                                                        'Leptin Deficiency or Dysfunction', 'Lesch-Nyhan syndrome', 'Leukemia', 'Leukoencephalopathy', 'Leukotriene C4-Synthesis Deficiency', 'Lewy body disease', 'Lipid peroxidation', 'Lipodystrophy', 'Lipoid Congenital Adrenal Hyperplasia', 'Lipoyltransferase 1 Deficiency', 'Liver disease', 'Long chain acyl-CoA dehydrogenase deficiency (LCAD)', 'Long-chain Fatty Acids', 'Long-chain-3-hydroxyacyl CoA dehydrogenase deficiency', 'Lung Cancer', 'Lymphosarcomatosis', 'Lysinuric protein intolerance', 'Macular degeneration', 'Major depressive disorder', 'Malaria', 'Malonyl-Coa decarboxylase deficiency', 'Maple syrup urine disease', 'Mastocytosis', 
                                                        'Maturity onset diabetes of the young', 'Meckels diverticulum', 'Medium Chain Acyl-CoA Dehydrogenase Deficiency', 'Megaloblastic anemia 1', 'Melanoma', 'Meningitis', 'Menkes disease', 'Menstrual cycle', 'Mental retardation', 'Metabolic encephalomyopathic crises', 'Metabolic syndrome', 'Metachromatic leukodystrophy', 'Metastatic melanoma', 'Methamphetamine (MAP) psychosis', 'Methanol poisoning', 'Methionine adenosyltransferase deficiency', 'Methotrexate treatment', 'Methyl formate exposure', 'Methylenetetrahydrofolate reductase deficiency', 'Methylmalonate semialdehyde dehydrogenase deficiency', 'Methylmalonic acidemia', 
                                                        'Methylmalonic acidemia and homocystinuria', 'Methylmalonic aciduria', 'Methylmalonic aciduria and homocystinuria', 'Methylmalonic aciduria mitochondrial encephelopathy Leigh-like', 'Methylmalonyl-CoA mutase deficiency', 'Mevalonic aciduria', 'Migraine', 'Mild cognitive impairment', 'Minimal brain dysfunction', 'Missing teeth', 'Mitochondrial Myopathy', 'Mitochondrial complex I deficiency due to ACAD9 deficiency', 'Mitochondrial encephalomyopaththy with elevanted methylmalonic acid', 'Mitochondrial phosphate carrier deficiency', 'Mitochondrial pyruvate carrier deficiency', 'Mitochondrial trifunctional protein deficiency', 
                                                        'Mitochondrial-encephalopathy-lactic acidosis-stroke', 'Molybdenium co-factor deficiency', 'Molybdenum cofactor deficiency', 'Monocarboxylate transporter 1 deficiency', 'Motor neuron disease', 'Mucopolysaccharidosis IVA ', 'Multi-infarct dementia', 'Multiple acyl-CoA dehydrogenase deficiency', 'Multiple carboxylase deficiency', 'Multiple myeloma', 'Multiple sclerosis', 'Multiple system atrophy', 'Mycobacterium tuberculosis', 'Myoadenylate deaminase deficiency', 'Myocardial infarction', 'Myoclonic epilepsy and ragged red fiber disease', 'Myopathic carnitine deficiency', 'Myopathy', 'Myopathy with lactic acidosis', 'N-acetylglutamate synthetase deficiency', 'Narcolepsy', 'Neonatal hepatitis', 'Nephrotic syndrome', 'Neu-Laxova Syndrome 1', 'Neuroblastoma', 'Neuroborreliosis', 'Neurodegenerative disease', 'Neuroinfection', 'Nicotinamide Adenine Dinucleotide Deficiency', "Non-Hodgkin's lymphoma", 'Nonalcoholic fatty liver disease', 'Nonketotic Hyperglycinemia', 'Nucleotide Depletion Syndrome', 'Obesity', 'Occipital Horn Syndrome', 'Oculocerebrorenal syndrome', 'Odontohypophosphatasia', 'Olivopontocerebral atrophy', 'Ornithine transcarbamylase deficiency', 'Orotic aciduria I', 'Osteoarthritis', 'Osteoporosis', 'Ovarian cancer', 'Oxidative stress', "Paget's disease", 'Pancreatic cancer', 'Panic disorder', 'Paraquat poisoning', "Parkinson's disease", 'Parkinsonian syndrome', 'Partial lipodystrophy', 'Patent Ductus Venosus', 'Pearson Syndrome', 'Pelizaeus Merzbacher Disease', 'Pellagra', 'Pendred Syndrome', 'Pentosuria', 'Perillyl alcohol administration for cancer treatment', 'Periodontal Probing Depth', 'Periodontal disease', 'Peripheral neuropathy', 'Peripheral vascular disease', 'Peritoneal dialysis', 'Peroxisomal biogenesis defect', 'Peroxisomal disorders', 'Pervasive developmental disorder not otherwise specified', 'Phenylketonuria', 'Pheochromocytoma', 'Phosphoenolpyruvate Carboxykinase Deficiency 1', 'Phosphoribosylpyrophosphate Synthetase Superactivity', 'Phosphoserine Aminotransferase Deficiency', 'Phosphoserine Phosphatase Deficiency', 
                                                        'Pituitary Hormone Deficiency', 'Polycystic ovary syndrome', 'Porphyria', 'Porphyria cutanea tarda', 'Portal vein obstruction', 'Postpartum depression', 'Prader-Willi syndrome', 'Preeclampsia', 'Pregnancy', 'Pregnene hydroxylation deficiency ', 'Premenstrual dysphoric disorder ', 'Prepartum depression', 'Preterm birth', 'Primary biliary cirrhosis', 'Primary hyperoxaluria', 'Primary hyperoxaluria I', 'Primary hyperoxaluria II', 'Primary hypomagnesemia', 'Progressive supranuclear palsy', 'Prolactinoma', 'Prolidase deficiency', 'Propionic acidemia', 'Proprotein Convertase 1/3 Deficiency', 'Prostate cancer', 'Prosthesis/Missing teeth', 'Proteinuria', 'Protoporphyria', 'Pseudohypoaldosteronism', 'Pseudoneonatal adrenoleukodystrophy', 'Pterin-4a carbinolamine dehydratase deficiency', 'Purine nucleoside phosphorylase deficiency ', 'Pyridoxamine 5-prime-phosphate oxidase deficiency', 'Pyridoxine-dependent epilepsy', 'Pyruvate carboxylase deficiency', 'Pyruvate dehydrogenase deficiency', 'Pyruvate dehydrogenase deficiency (E1)', 'Pyruvate dehydrogenase phosphatase deficiency', 'Quetiapine poisoning', 'Rachialgia', 'Refractory anemia', 'Refractory localization-related epilepsy', "Refsum's disease", 'Renal tubular acidosis', 'Rett syndrome', "Reye's syndrome", 'Rhabdomyolysis', 'Rheumatoid arthritis', 'Rhinitis', 'Rhizomelic chondrodysplasia punctata', 'Ribose-5-phosphate isomerase deficiency', 'SC4MOL deficiency', 'Saccharopinuria', 'Salla disease', 'Sarcoma', 'Sarcosinemia', 'Schistosomiasis', 'Schizophrenia', 'Segawa Syndrome', 'Seizures', 'Sengers syndrome', 'Sepiapterin reductase deficiency', 'Sepsis', 'Septic shock', 'Serine deficiency syndrome', 'Short Chain Acyl-Coa Dehydrogenase Deficiency', 'Short bowel syndrome', 'Short-chain L-3-hydroxyacyl-CoA dehydrogenase deficiency', 'Short/branched chain acyl-CoA dehydrogenase deficiency', 'Sialidosis', 'Sickle cell anemia', 'Sitosterolemia', 'Sjögren-Larsson syndrome', 'Sleep apnea', 'Small bowel bacterial overgrowth syndrome', 'Small intestinal malabsorption', 'Smith-Lemli-Opitz syndrome', 'Smoking', 'Sodium nitrate consumption', 'Spina Bifida', 'Spondyloenchondrodysplasia', 'Sporadic amyotrophic lateral sclerosis', 'Stomach cancer', 'Stress', 'Stroke', 'Subarachnoid hemorrhage', 
                                                        'Succinic semialdehyde dehydrogenase deficiency', 'Sucrase-isomaltase deficiency', 'Sulfite oxidase deficiency', 'Supradiaphragmatic malignancy', 'Supragingival Calculus', 'Supragingival Plaque', 'Temporomandibular joint disorder', 'Terminal aldosterone biosynthesis defects', 'Testicular adrenal rest tumors', 'Tetrahydrofuran exposure', 
                                                        'Thymidine phosphorylase deficiency', 'Thymidine treatment', 'Thyroid cancer ', 'Tic disorder', 'Tooth Decay', 'Transaldolase deficiency', 'Transcobalamin II deficiency', 'Transurethral resection of the prostate', 'Trauma', 'Traumatic brain injury', 'Trimethylaminuria', 'Tryptophanuria with dwarfism', 'Tuberculosis', 'Tuberculous meningitis', 'Tyrosinemia', 'Tyrosinemia I', 'Ulcerative colitis', 'Uremia', 'Urocanase deficiency', 'Variegate porphyria', 'Very Long Chain Acyl-CoA Dehydrogenase Deficiency', 'Vessel occlusion', 'Viral infection', 'Vitamin B12 deficiency', 'Vitamin E deficiency', 'Vitiligo', "Wilson's disease", 'Wolcott-Rallison syndrome', 'Wolfram syndrome 1', 'Woodhouse-Sakati syndrome', 'X-linked ichthyosis', 'XY sex reversal', 'Xanthinuria type 1', 'Xanthinuria type II', 'beta-Mannosidosis', 'congenital disorder of glycosylation CDG-Ia'], 
                                                        default=['Leukemia'], help=help_disease)

help_db_cutoff = help_texts['slider_database']
database_cutoff = st.sidebar.slider("Select cutoff for STITCH database score", 0, 1000, 993, help=help_db_cutoff)

help_exp_cutoff = help_texts['slider_experiment']
experiment_cutoff = st.sidebar.slider("Select cutoff for STITCH experimental score", 0, 1000, 993, help=help_exp_cutoff)

help_pred_cutoff = help_texts['slider_prediction']
prediction_cutoff = st.sidebar.slider("Select cutoff for STITCH prediction score", 0, 1000, 700, help=help_pred_cutoff)

help_comb_cutoff = help_texts['slider_combined']
combined_cutoff = st.sidebar.slider("Select cutoff for STITCH combined score", 0, 1000, 900, help=help_comb_cutoff)

help_exo = help_texts['checkbox_exo']
include_exo = st.sidebar.checkbox("Include exogenous metabolites", value=False, help=help_exo)

help_purpose = help_texts['radio_purpose']
selected_purpose = st.sidebar.radio("Select purpose", ["Table", "Graph"], help=help_purpose)

if selected_purpose == "Table":

    number = st.sidebar.number_input("Maximum rows to display in table", value=100)

if st.sidebar.button("Retrieve"):

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    if selected_purpose == "Table":

        my_bar.progress(20, text='loading data')
         
        subgraph = n4j.get_subgraph(
            cellular_locations,
            tissue_locations,
            biospecimen_locations,
            diseases,
            pathways,
            database_cutoff,
            experiment_cutoff, 
            prediction_cutoff,
            combined_cutoff,
            include_exo,
            output="table"
        )

        my_bar.progress(80, text='PROCESSING')


        subgraph.rename(columns={'Symbol': 'Protein', 'Database': 'DatabaseScore', 'Experiment': 'ExperimentalScore',
                                'CellLoc': 'Cellular Location', 'TissueLoc': 'Tissue Location', 'BiospecLoc': 'Biospecimen Location',
                                 }, inplace=True)
        
        # convert protein hmdb and uniprot to links
        subgraph['HMDB'] = subgraph['HMDB'].apply(lambda x: f'https://hmdb.ca/metabolites/{x}')
        subgraph['Uniprot'] = [x.split(':')[1] for x in subgraph['Uniprot']]
        subgraph['Uniprot'] = subgraph['Uniprot'].apply(lambda x: f"https://www.uniprot.org/uniprot/{x}")

        #reorder columns that Uniprot column is in the fourth position
        subgraph = subgraph[[ 'MetName','HMDB', 'Protein', 'Uniprot', 'ProtName', 'Cellular Location', 'Tissue Location', 'Biospecimen Location', 'Diseases', 'Pathways', 'DatabaseScore', 'ExperimentalScore',
       'Prediction', 'Combined']]
        
        my_bar.progress(100, text='DONE')
        my_bar.empty()

        subgraph_table = subgraph

        if subgraph.shape[0] > number:
            subgraph_table = subgraph.head(number)

        st.data_editor(
            subgraph_table,
            column_config={
            'HMDB': st.column_config.LinkColumn(
                'HMDB', 
                help="The top trending Streamlit apps",
                display_text="https://hmdb\.ca/metabolites/(HMDB\d+)", 
            ),
            'Uniprot': st.column_config.LinkColumn(
                'Uniprot', 
                help="The top trending Streamlit apps",
                display_text="https://www\.uniprot\.org/uniprot/(.*)", 
            ),


            }
        )

        # st.dataframe(subgraph)
        
        # Download button
        csv = subgraph.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to base64 encoding
        href = f'<a href="data:file/csv;base64,{b64}" download="metalinks_data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)


        # Summary box
        num_rows = len(subgraph.index)
        num_unique_metabolites = subgraph['HMDB'].nunique()
        num_unique_proteins = subgraph['Protein'].nunique()

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        # Define custom color palette
        colors = ["#932a61", "#512D55"]

        # Summary table
        with col1:
            summary_data = {
                'Metrics': ['Number of Interactions', 'Number of unique metabolite ligands', 'Number of unique protein receptors'],
                'Values': [num_rows, num_unique_metabolites, num_unique_proteins]
            }
            summary_df = pd.DataFrame(summary_data)

            style = summary_df.style.hide(axis="index")
            style.hide(axis="columns")
            st.write(style.to_html(), unsafe_allow_html=True)


        # Bar chart - CellLoc
        with col2:
            cellloc_counts = subgraph['Cellular Location'].explode().value_counts()
            cellloc_percentages = cellloc_counts / len(subgraph) * 100

            fig_cellloc, ax_cellloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=cellloc_percentages.index, y=cellloc_percentages.values, ax=ax_cellloc, palette=colors)
            ax_cellloc.set_ylabel("Percentage")
            #ax_cellloc.set_title("Cellular Location Distribution")
            ax_cellloc.set_xticklabels(ax_cellloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_cellloc)

        # Bar chart - TissueLoc
        with col3:
            tissueloc_counts = subgraph['Tissue Location'].explode().value_counts()
            tissueloc_percentages = tissueloc_counts / len(subgraph) * 100

            fig_tissueloc, ax_tissueloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=tissueloc_percentages.index, y=tissueloc_percentages.values, ax=ax_tissueloc, palette=colors)
            ax_tissueloc.set_ylabel("Percentage")
            #ax_tissueloc.set_title("Tissue Location Distribution")
            ax_tissueloc.set_xticklabels(ax_tissueloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_tissueloc)

        # Bar chart - BiospecLoc
        with col4:
            biospecloc_counts = subgraph['Biospecimen Location'].explode().value_counts()
            biospecloc_percentages = biospecloc_counts / len(subgraph) * 100

            fig_biospecloc, ax_biospecloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=biospecloc_percentages.index, y=biospecloc_percentages.values, ax=ax_biospecloc, palette=colors)
            ax_biospecloc.set_ylabel("Percentage")
            #ax_biospecloc.set_title("Biospecimen Location Distribution")
            ax_biospecloc.set_xticklabels(ax_biospecloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_biospecloc)

    elif selected_purpose == "Graph":

        my_bar.progress(20, text='loading data')

        subgraph = n4j.get_subgraph(            
            cellular_locations,
            tissue_locations,
            biospecimen_locations,
            diseases,
            pathways,
            database_cutoff,
            experiment_cutoff, 
            prediction_cutoff,
            combined_cutoff,
            include_exo,
            output="graph")
    
        my_bar.progress(80, text='PROCESSING')
        # components.html(
        
        html_code = ''' 
        <head>
            <script src="https://cdn.drugst.one/latest/drugstone.js"></script>
            <link rel="stylesheet" href="https://cdn.drugst.one/latest/styles.css">

        </head>

        <drugst-one
            id='drugstone-component-id'
            groups='{
                "nodeGroups":{
                    "gene":{"type":"protein",
                            "color":"#512D55",
                            "font":{"color":"#f0f0f0"},
                            "groupName":"Protein","shape":"circle"},
                    "foundDrug":{"type":"metabolite",
                                "color":"#932a61",
                                "font":{"color":"#000000"},
                                "groupName":"Metabolite",
                                "shape":"diamond"},
                    "metabolite":{"type":"drug",
                                    "color":"#932a61",
                                    "font":{"color":"#f0f0f0"},
                                    "groupName":"Metabolite",
                                    "shape":"diamond"}
                                },

                "edgeGroups":{
                    "default":{"color":"#000000","groupName":"default edge"},
                    
                            }
                    }'
            config='{
                "identifier":"symbol",
                "title":"MetalinksKG - metabolite-mediated cell-cell communication",
                "nodeShadow":true,
                "edgeShadow":false,
                showSidebar: "right",
                showOverview: true,
                showQuery: true,
                showItemSelector: false,
                showSimpleAnalysis: false,
                showAdvAnalysis: false,
                showConnectGenes: false,
                showSelection: false,
                showTasks: false,
                showNetworkMenu: false,
                "autofillEdges":false,
                "interactionDrugProtein":"ChEMBL",
                "activateNetworkMenuButtonAdjacentDrugs":false,
                "physicsOn":false,
                "activateNetworkMenuButtonAdjacentDisorderDrugs":false}'
            network='{}'>

            
        </drugst-one>

        <style>
        :root {
            --drgstn-primary: #932a61;
            --drgstn-secondary: #512D55;
            --drgstn-success: #48C774;
            --drgstn-warning: #ffdd00;
            --drgstn-danger: #ff2744;
            --drgstn-background: #f8f9fa;
            --drgstn-panel: #ffffff;
            --drgstn-info: #61c43d;
            --drgstn-text-primary: #151515;
            --drgstn-text-secondary: #eeeeee;
            --drgstn-border: rgba(0, 0, 0, 0.2);
            --drgstn-tooltip: rgba(74, 74, 74, 0.9);
            --drgstn-panel-secondary: #FFFFFF;
            --drgstn-height: 800px;
            --drgstn-font-family: Helvetica Neue, sans-serif;
        }
        </style>
        '''
   
        nodes = subgraph[0]
        nodes.extend(subgraph[1])
        network_data = {
            "nodes": nodes,
            "edges": subgraph[2]
        }
        html_code = html_code.replace("'{}'", json.dumps(network_data))
        html_code = html_code.replace("network={","network='{")
        html_code = html_code.replace("}]}>", "}]}'>")

        my_bar.progress(100, text='DONE')
        my_bar.empty()

        st.components.v1.html(html_code, height=1200, width=1200)

                # "showOverview": true,
                # "showQuery": False,
                # "showItemSelector": true,
                # "showSimpleAnalysis": false,
                # "showAdvAnalysis": true,
                # "showSelection": true,
                # "showTasks": off,
                # "showNetworkMenu": off,
                # "showLegend": true,
                # "showConnectGenes": false,

url = 'https://github.com/biocypher/metalinks'
st.sidebar.markdown(f'[Documentation]({url})')