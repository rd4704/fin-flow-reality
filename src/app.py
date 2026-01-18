import streamlit as st
import pandas as pd
from components.file_upload import upload_file
from components.visualizations import plot_dual_cash_flow
from utils.cash_flow_analyzer import calculate_metrics, get_top_offenders


def main():
    # Page configuration
    st.set_page_config(
        page_title="FinFlow Reality - Cash Flow Intelligence",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional fintech theme
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E3A8A;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #64748B;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #F8FAFC;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3B82F6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">💰 FinFlow Reality</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform Invoice Chaos into Cash Flow Clarity</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # File upload
    transactions_df = upload_file()
    
    if transactions_df is not None:
        # Reality toggle and delay slider
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔧 Reality Settings")
        
        show_reality = st.sidebar.checkbox("Enable Reality View", value=True, 
                                          help="Compare optimistic vs realistic cash flow projections")
        
        delay_days = st.sidebar.slider(
            "Customer Delay Factor (Days)",
            min_value=0,
            max_value=90,
            value=30,
            step=5,
            help="Average days customers delay payment on pending invoices"
        )
        
        # Peppol E-Invoicing info
        st.sidebar.markdown("---")
        with st.sidebar.expander("💡 About Peppol E-Invoicing"):
            st.markdown("""
            **Peppol E-Invoicing** enables:
            - ✅ Real-time payment tracking
            - ✅ Automated reconciliation
            - ✅ Reduced payment delays
            - ✅ Better cash flow predictability
            
            Countries like Singapore mandate Peppol for B2G transactions, 
            helping SMEs get paid faster and plan better.
            """)
        
        # Calculate metrics
        metrics = calculate_metrics(transactions_df, delay_days)
        
        # Display key metrics
        st.markdown("### 📊 Financial Health Dashboard")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Current Balance",
                value=f"${metrics['current_balance']:,.0f}",
                delta=None,
                help="Total balance from all paid transactions"
            )
        
        with col2:
            delta_val = -metrics['projected_gap'] if show_reality else None
            st.metric(
                label="Projected Gap (30 Days)",
                value=f"${metrics['projected_gap']:,.0f}",
                delta=f"${delta_val:,.0f}" if delta_val else None,
                delta_color="inverse",
                help="Difference between optimistic and reality projections"
            )
        
        with col3:
            st.metric(
                label="Risk Level",
                value=metrics['risk_level'],
                delta=None,
                help="Risk assessment based on reality projection"
            )
        
        # Dual-line visualization
        st.markdown("### 📈 Cash Flow Projection: Optimistic vs Reality")
        
        if show_reality:
            st.info(f"💡 **Reality Mode Active**: Pending invoices delayed by **{delay_days} days**. Toggle off to see optimistic view.")
        else:
            st.success("✅ **Optimistic Mode**: All invoices assumed paid on time.")
        
        plot_dual_cash_flow(transactions_df, delay_days=delay_days, show_reality=show_reality)
        
        # Top offenders table
        st.markdown("### 🎯 Top Offenders: Liquidity Locked by Customer")
        
        top_offenders = get_top_offenders(transactions_df, top_n=5)
        
        if len(top_offenders) > 0:
            st.dataframe(
                top_offenders.style.format({'Locked Amount': '${:,.0f}'}),
                use_container_width=True,
                hide_index=True
            )
            
            total_locked = top_offenders['Locked Amount'].sum()
            st.caption(f"💰 **Total Liquidity Locked**: ${total_locked:,.0f} across {len(top_offenders)} customers")
        else:
            st.success("🎉 No pending invoices! All customers have paid on time.")
        
        # Transaction data preview
        with st.expander("📋 View Transaction Data"):
            st.dataframe(
                transactions_df.style.format({'Amount': '${:,.0f}'}),
                use_container_width=True
            )
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(transactions_df))
            with col2:
                paid_count = len(transactions_df[transactions_df['Status'] == 'Paid'])
                st.metric("Paid", paid_count)
            with col3:
                pending_count = len(transactions_df[transactions_df['Status'] == 'Pending'])
                st.metric("Pending", pending_count)
    
    else:
        # Welcome screen when no data loaded
        st.info("👈 **Get Started**: Upload your transaction CSV or load sample data from the sidebar.")
        
        st.markdown("### 🚀 What You'll Get")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📊 Dual-Line Cash Flow
            - **Optimistic View**: Assumes all invoices paid on time
            - **Reality View**: Accounts for customer payment delays
            - **Cash Crunch Alerts**: Highlights periods of negative balance
            """)
        
        with col2:
            st.markdown("""
            #### 💡 Business Intelligence
            - **Top Offenders**: Customers with most pending payments
            - **Liquidity Analysis**: Track locked cash flow
            - **Risk Assessment**: Real-time financial health monitoring
            """)
        
        st.markdown("### 📋 CSV Format Required")
        st.code("""Date,Description,Amount,Type,Status
2023-01-01,Acme Corp SG,5000,Inflow,Paid
2023-01-05,Office Supplies Co,-1500,Outflow,Paid
2023-01-10,TechVision Ltd,12000,Inflow,Pending""", language="csv")


if __name__ == "__main__":
    main()