import streamlit as st
import pandas as pd
import plotly.express as px
from src.pipeline import generate_events,train_and_evaluate,explain_rules

st.set_page_config(page_title='CareShield AI | Access Risk Lab',page_icon='🛡️',layout='wide')
st.markdown('''<style>
.stApp {background: #0b1220;color:#edf2ff} [data-testid="stMetric"] {background:#15233a;padding:16px;border-radius:14px;border:1px solid #273b58}
h1,h2,h3 {color:#e9f2ff!important} .stCaption {color:#a5b4ca!important}
</style>''',unsafe_allow_html=True)
st.title('🛡️ CareShield AI')
st.caption('Healthcare Access Risk Lab  •  Synthetic data  •  Research demonstration, not a clinical or security decision system')

@st.cache_data(show_spinner=False)
def dataset(n,seed): return generate_events(n,seed)
@st.cache_resource(show_spinner='Training a reproducible baseline…')
def evaluation(n,seed): return train_and_evaluate(dataset(n,seed))
with st.sidebar:
 st.header('Experiment controls')
 n=st.slider('Synthetic access events',1000,15000,5000,1000)
 seed=st.number_input('Random seed',min_value=0,max_value=99999,value=42)
 st.info('All staff and patient identifiers are synthetic. No hospital systems are connected.')
df=dataset(n,seed)
model,metrics,test=evaluation(n,seed)
test['risk_factors']=test.apply(explain_rules,axis=1)

k1,k2,k3,k4=st.columns(4)
k1.metric('Events analysed',f'{n:,}')
k2.metric('Synthetic alerts',f"{df.synthetic_alert.sum():,}")
k3.metric('Holdout average precision',f"{metrics['average_precision']:.3f}")
k4.metric('Holdout false positives',metrics['false_positives'])

st.warning('Important: Synthetic alert labels were generated from behavioural rules. High model accuracy does NOT establish effectiveness against real insider threats.')
left,right=st.columns(2)
with left:
 st.subheader('Access activity over time')
 daily=df.assign(day=df.timestamp.dt.date).groupby('day',as_index=False).agg(events=('event_id','count'),alerts=('synthetic_alert','sum'))
 st.plotly_chart(px.line(daily,x='day',y=['events','alerts'],template='plotly_dark',labels={'value':'Events','day':'Date'}),use_container_width=True)
with right:
 st.subheader('Scenario alerts by role')
 role=df.groupby('role',as_index=False).agg(alerts=('synthetic_alert','sum'))
 st.plotly_chart(px.bar(role,x='role',y='alerts',template='plotly_dark',color='alerts',color_continuous_scale='Teal'),use_container_width=True)

st.subheader('Investigate held-out events')
min_risk=st.slider('Minimum predicted risk',0.0,1.0,0.5,0.05)
roles=st.multiselect('Role',sorted(test.role.unique()),default=sorted(test.role.unique()))
view=test[(test.predicted_risk>=min_risk)&(test.role.isin(roles))].sort_values('predicted_risk',ascending=False)
cols=['timestamp','event_id','staff_id','patient_token','role','predicted_risk','synthetic_alert','risk_factors']
st.dataframe(view[cols],use_container_width=True,hide_index=True,column_config={'predicted_risk':st.column_config.ProgressColumn('Predicted risk',min_value=0,max_value=1,format='%.2f')})
st.download_button('Export filtered investigations (CSV)',view[cols].to_csv(index=False).encode(),file_name='careshield_investigations.csv',mime='text/csv')
with st.expander('Evaluation and limitations'):
 st.write('Chronological 70/30 holdout; preprocessing is fit on training data only. No patient-level or staff-level independence guarantee. Repeated staff IDs may occur across both sets.')
 st.json(metrics)
 st.write('The risk factors column explains the synthetic scenario rules, not the Random Forest prediction. Do not interpret it as SHAP or a causal explanation.')
 st.write('For real deployment: obtain lawful, governed audit logs; validate incident labels independently; assess bias, calibration, drift, false alarms and human review requirements.')
