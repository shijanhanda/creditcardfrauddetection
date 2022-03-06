import streamlit as st
import os
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

#taking required transaction and identity columns required
transaction_columnname=['TransactionID','TransactionDT','TransactionAmt','ProductCD','card1','card2','card3','card4','card5','card6','addr1','addr2','P_emaildomain','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','D1','D10','D15','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28','V29','V30','V31','V32','V33','V34','V53','V54','V55','V56','V57','V58','V59','V60','V61','V62','V63','V64','V65','V66','V67','V68','V69','V70','V71','V72','V73','V74','V75','V76','V77','V78','V79','V80','V81','V82','V83','V84','V85','V86','V87','V88','V89','V90','V91','V92','V93','V94','V95','V96','V97','V98','V99','V100','V101','V102','V103','V104','V105','V106','V107','V108','V109','V110','V111','V112','V113','V114','V115','V116','V117','V118','V119','V120','V121','V122','V123','V124','V125','V126','V127','V128','V129','V130','V131','V132','V133','V134','V135','V136','V137','V279','V280','V281','V282','V283','V284','V285','V286','V287','V288','V289','V290','V291','V292','V293','V294','V295','V296','V297','V298','V299','V300','V301','V302','V303','V304','V305','V306','V307','V308','V309','V310','V311','V312','V313','V314','V315','V316','V317','V318','V319','V320','V321']
identity_columnname =['TransactionID', 'id_01', 'id_02', 'id_03', 'id_04', 'id_05', 'id_06','id_07', 'id_08', 'id_09', 'id_10', 'id_11', 'id_12', 'id_13', 'id_14','id_15', 'id_16', 'id_17', 'id_18', 'id_19', 'id_20', 'id_21', 'id_22','id_23', 'id_24', 'id_25', 'id_26', 'id_27', 'id_28', 'id_29', 'id_30','id_31', 'id_32', 'id_33', 'id_34', 'id_35', 'id_36', 'id_37', 'id_38','DeviceType', 'DeviceInfo']

#reading csv files as input
transac_file = st.file_uploader("Upload Transaction File", type=["csv","xlsx","xls"])
identity_file = st.file_uploader("Upload Identity File", type=["csv","xlsx","xls"])

#Method to compute imputation values for null fields in input files and saving in cache
@st.cache
def compute_impute_values():
     dict_median={'TransactionID':'3916894.0','TransactionDT':'27204658.0','TransactionAmt':'67.95','card1':'9803.0','card2':'369.0','card3':'150.0','card5':'226.0','addr1':'299.0','addr2':'87.0','dist1':'8.0','dist2':'44.0','C1':'1.0','C2':'1.0','C3':'0.0','C4':'0.0','C5':'0.0','C6':'1.0','C7':'0.0','C8':'0.0','C9':'1.0','C10':'0.0','C11':'1.0','C12':'0.0','C13':'3.0','C14':'1.0','D1':'5.0','D2':'112.0','D3':'7.0','D4':'21.0','D5':'8.0','D6':'0.0','D7':'0.0','D8':'37.70833206176758','D9':'0.6666659712791443','D10':'10.0','D11':'102.0','D12':'0.0','D13':'0.0','D14':'0.0','D15':'48.0','V1':'1.0','V2':'1.0','V3':'1.0','V4':'1.0','V5':'1.0','V6':'1.0','V7':'1.0','V8':'1.0','V9':'1.0','V10':'0.0','V11':'0.0','V12':'1.0','V13':'1.0','V14':'1.0','V15':'0.0','V16':'0.0','V17':'0.0','V18':'0.0','V19':'1.0','V20':'1.0','V21':'0.0','V22':'0.0','V23':'1.0','V24':'1.0','V25':'1.0','V26':'1.0','V27':'0.0','V28':'0.0','V29':'0.0','V30':'0.0','V31':'0.0','V32':'0.0','V33':'0.0','V34':'0.0','V35':'1.0','V36':'1.0','V37':'1.0','V38':'1.0','V39':'0.0','V40':'0.0','V41':'1.0','V42':'0.0','V43':'0.0','V44':'1.0','V45':'1.0','V46':'1.0','V47':'1.0','V48':'0.0','V49':'0.0','V50':'0.0','V51':'0.0','V52':'0.0','V53':'1.0','V54':'1.0','V55':'1.0','V56':'1.0','V57':'0.0','V58':'0.0','V59':'0.0','V60':'0.0','V61':'1.0','V62':'1.0','V63':'0.0','V64':'0.0','V65':'1.0','V66':'1.0','V67':'1.0','V68':'0.0','V69':'0.0','V70':'0.0','V71':'0.0','V72':'0.0','V73':'0.0','V74':'0.0','V75':'1.0','V76':'1.0','V77':'1.0','V78':'1.0','V79':'0.0','V80':'0.0','V81':'0.0','V82':'1.0','V83':'1.0','V84':'0.0','V85':'0.0','V86':'1.0','V87':'1.0','V88':'1.0','V89':'0.0','V90':'0.0','V91':'0.0','V92':'0.0','V93':'0.0','V94':'0.0','V95':'0.0','V96':'0.0','V97':'0.0','V98':'0.0','V99':'0.0','V100':'0.0','V101':'0.0','V102':'0.0','V103':'0.0','V104':'0.0','V105':'0.0','V106':'0.0','V107':'1.0','V108':'1.0','V109':'1.0','V110':'1.0','V111':'1.0','V112':'1.0','V113':'1.0','V114':'1.0','V115':'1.0','V116':'1.0','V117':'1.0','V118':'1.0','V119':'1.0','V120':'1.0','V121':'1.0','V122':'1.0','V123':'1.0','V124':'1.0','V125':'1.0','V126':'0.0','V127':'0.0','V128':'0.0','V129':'0.0','V130':'0.0','V131':'0.0','V132':'0.0','V133':'0.0','V134':'0.0','V135':'0.0','V136':'0.0','V137':'0.0','V138':'0.0','V139':'1.0','V140':'1.0','V141':'0.0','V142':'0.0','V143':'0.0','V144':'0.0','V145':'0.0','V146':'0.0','V147':'0.0','V148':'1.0','V149':'1.0','V150':'1.0','V151':'1.0','V152':'1.0','V153':'1.0','V154':'1.0','V155':'1.0','V156':'1.0','V157':'1.0','V158':'1.0','V159':'0.0','V160':'0.0','V161':'0.0','V162':'0.0','V163':'0.0','V164':'0.0','V165':'0.0','V166':'0.0','V167':'0.0','V168':'0.0','V169':'0.0','V170':'1.0','V171':'1.0','V172':'0.0','V173':'0.0','V174':'0.0','V175':'0.0','V176':'1.0','V177':'0.0','V178':'0.0','V179':'0.0','V180':'0.0','V181':'0.0','V182':'0.0','V183':'0.0','V184':'0.0','V185':'0.0','V186':'1.0','V187':'1.0','V188':'1.0','V189':'1.0','V190':'1.0','V191':'1.0','V192':'1.0','V193':'1.0','V194':'1.0','V195':'1.0','V196':'1.0','V197':'1.0','V198':'1.0','V199':'1.0','V200':'1.0','V201':'1.0','V202':'0.0','V203':'0.0','V204':'0.0','V205':'0.0','V206':'0.0','V207':'0.0','V208':'0.0','V209':'0.0','V210':'0.0','V211':'0.0','V212':'0.0','V213':'0.0','V214':'0.0','V215':'0.0','V216':'0.0','V217':'0.0','V218':'0.0','V219':'0.0','V220':'0.0','V221':'1.0','V222':'1.0','V223':'0.0','V224':'0.0','V225':'0.0','V226':'0.0','V227':'0.0','V228':'1.0','V229':'1.0','V230':'1.0','V231':'0.0','V232':'0.0','V233':'0.0','V234':'0.0','V235':'0.0','V236':'0.0','V237':'0.0','V238':'0.0','V239':'0.0','V240':'1.0','V241':'1.0','V242':'1.0','V243':'1.0','V244':'1.0','V245':'1.0','V246':'1.0','V247':'1.0','V248':'1.0','V249':'1.0','V250':'1.0','V251':'1.0','V252':'1.0','V253':'1.0','V254':'1.0','V255':'1.0','V256':'1.0','V257':'1.0','V258':'1.0','V259':'1.0','V260':'1.0','V261':'1.0','V262':'1.0','V263':'0.0','V264':'0.0','V265':'0.0','V266':'0.0','V267':'0.0','V268':'0.0','V269':'0.0','V270':'0.0','V271':'0.0','V272':'0.0','V273':'0.0','V274':'0.0','V275':'0.0','V276':'0.0','V277':'0.0','V278':'0.0','V279':'0.0','V280':'0.0','V281':'0.0','V282':'1.0','V283':'1.0','V284':'0.0','V285':'0.0','V286':'0.0','V287':'0.0','V288':'0.0','V289':'0.0','V290':'1.0','V291':'1.0','V292':'1.0','V293':'0.0','V294':'0.0','V295':'0.0','V296':'0.0','V297':'0.0','V298':'0.0','V299':'0.0','V300':'0.0','V301':'0.0','V302':'0.0','V303':'0.0','V304':'0.0','V305':'1.0','V306':'0.0','V307':'0.0','V308':'0.0','V309':'0.0','V310':'0.0','V311':'0.0','V312':'0.0','V313':'0.0','V314':'0.0','V315':'0.0','V316':'0.0','V317':'0.0','V318':'0.0','V319':'0.0','V320':'0.0','V321':'0.0','V322':'0.0','V323':'0.0','V324':'0.0','V325':'0.0','V326':'0.0','V327':'0.0','V328':'0.0','V329':'0.0','V330':'0.0','V331':'0.0','V332':'0.0','V333':'0.0','V334':'0.0','V335':'0.0','V336':'0.0','V337':'0.0','V338':'0.0','V339':'0.0','id-01':'-5.0','id-02':'133189.5','id-03':'0.0','id-04':'0.0','id-05':'0.0','id-06':'0.0','id-07':'12.0','id-08':'-33.0','id-09':'0.0','id-10':'0.0','id-11':'100.0','id-13':'27.0','id-14':'-300.0','id-17':'166.0','id-18':'15.0','id-19':'321.0','id-20':'484.0','id-21':'576.0','id-22':'14.0','id-24':'11.0','id-25':'321.0','id-26':'147.0','id-32':'24.0'}

     dict_mode={'ProductCD':'W','card4':'visa','card6':'debit','P_emaildomain':'gmail.com','R_emaildomain':'gmail.com','M1':'T','M2':'T','M3':'T','M4':'M0','M5':'F','M6':'F','M7':'F','M8':'F','M9':'T','id-12':'NotFound','id-15':'Found','id-16':'Found','id-23':'IP_PROXY:TRANSPARENT','id-27':'Found','id-28':'Found','id-29':'Found','id-30':'Windows 10','id-31':'chrome 70.0','id-33':'1920x1080','id-34':'match_status:2','id-35':'T','id-36':'F','id-37':'T','id-38':'F','DeviceType':'desktop','DeviceInfo':'Windows'}
     return dict_median,dict_mode

if transac_file and identity_file:
        df_tra_test=pd.read_csv(transac_file,low_memory=False)
        df_ide_test=pd.read_csv(identity_file,low_memory=False)
        missingtranscolumns =[]
        missingidentcolumns =[]
        for i in transaction_columnname:
            if i not in df_tra_test.columns:
                missingtranscolumns.append(i)
               
        for i in identity_columnname:
            if i not in df_ide_test.columns:
                missingidentcolumns.append(i)

        if missingtranscolumns:
            st.write(' These columns seem to be missing in the uploaded transaction file: ',missingtranscolumns)
            st.write('please reload page and try again')

        elif missingidentcolumns:
            st.write(' These columns seem to be missing in the uploaded identity file: ',missingidentcolumns)
            st.write('please reload page and try again') 

        else:        
            df_test = pd.merge(df_tra_test, df_ide_test,on='TransactionID', how='left')
            df_test=df_test[transaction_columnname]
            st.write(df_test)

            dict_median,dict_mode=compute_impute_values()

            imputemedian=df_test.select_dtypes(exclude=['object']).columns
            imputemode=df_test.select_dtypes(include=['object']).columns
            for index,colval in enumerate(imputemedian):
                df_test[colval].fillna(dict_median[colval],inplace=True)
            for index,colval in enumerate(imputemode):
                df_test[colval].fillna(dict_mode[colval],inplace=True)


            import joblib
            ohe=joblib.load('ohe.save')
            df_encoded=ohe.transform(df_test[['ProductCD', 'card4', 'card6']])
            df_enc=pd.DataFrame(data=df_encoded,columns=['ProductCD_W','ProductCD_C','ProductCD_R','ProductCD_H','card40','card41','card42','card60','card61','card62'])
            df_test.drop(['ProductCD', 'card4', 'card6','P_emaildomain'],inplace=True,axis=1)
            df_test= pd.concat([df_test,df_enc],axis=1)

            #loading model pickle file
            model=pickle.load(open('model_DecisionTreeClassifier.pkl','rb'))
            outputs=model.predict(df_test)
            
            for id,output in zip(df_test['TransactionID'],outputs):
                if output==0:
                    st.write('Transaction id: '+str(id)+' is not fraudelent')
                else:
                    st.write('Transaction id: '+str(id)+' is fraudelent')