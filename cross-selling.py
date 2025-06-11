import streamlit as st
import pandas as pd

@st.cache_data
def load_rules(path='association_rules.csv'):
    df = pd.read_csv(path)
    df['antecedents'] = df['antecedents'].apply(eval).apply(set)
    df['consequents'] = df['consequents'].apply(eval).apply(set)
    return df

rules = load_rules()

st.title("Cross-Selling Product Recommendations")

#Flattening antecedent sets to unique products for selection
all_antecedents = set()
for antecedent_set in rules['antecedents']:
    all_antecedents.update(antecedent_set)
all_antecedents = sorted(list(all_antecedents))

selected_product = st.selectbox("Select a product you want to cross-sell from:", all_antecedents)

#Filtering rules where selected product is in antecedents
matched_rules = rules[rules['antecedents'].apply(lambda x: selected_product in x)]

if matched_rules.empty:
    st.warning(f"No cross-sell recommendations found for '{selected_product}'.")
else:
    st.write(f"Top cross-sell recommendations for **{selected_product}**:")

    #Sorting by confidence, lift or support
    sort_option = st.selectbox("Sort recommendations by:", ['confidence', 'lift', 'support'])
    matched_rules = matched_rules.sort_values(by=sort_option, ascending=False).head(10)

    for idx, row in matched_rules.iterrows():
        consequents = ', '.join(row['consequents'])
        st.markdown(f"**Buy along with:** {consequents}")
        st.markdown(f"- Confidence: {row['confidence']:.2f}")
        st.markdown(f"- Lift: {row['lift']:.2f}")
        st.markdown(f"- Support: {row['support']:.3f}")
        st.markdown("---")

st.info("Use these cross-sell suggestions to upsell related products to customers.")
