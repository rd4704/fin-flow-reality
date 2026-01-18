import plotly.graph_objs as go
import pandas as pd
import streamlit as st
from utils.cash_flow_analyzer import calculate_cumulative_cash_flow


def plot_dual_cash_flow(transactions, delay_days=0, show_reality=True):
    """
    Plot dual-line cash flow: Optimistic vs Reality with cash crunch highlighting.
    
    Args:
        transactions (DataFrame): Transaction data.
        delay_days (int): Customer delay factor in days.
        show_reality (bool): Whether to show the reality line.
    """
    # Calculate both scenarios
    dates_opt, balance_opt = calculate_cumulative_cash_flow(transactions, delay_days=0, reality_mode=False)
    dates_real, balance_real = calculate_cumulative_cash_flow(transactions, delay_days=delay_days, reality_mode=True)
    
    fig = go.Figure()
    
    # Line A: Optimistic (all invoices paid on time)
    fig.add_trace(go.Scatter(
        x=dates_opt,
        y=balance_opt,
        mode='lines',
        name='📈 Optimistic (On-Time Payment)',
        line=dict(color='#2ECC71', width=2),
        hovertemplate='<b>Optimistic</b><br>Date: %{x}<br>Balance: $%{y:,.0f}<extra></extra>'
    ))
    
    # Line B: Reality (with delay factor)
    if show_reality:
        fig.add_trace(go.Scatter(
            x=dates_real,
            y=balance_real,
            mode='lines',
            name='⚠️ Reality (With Delays)',
            line=dict(color='#E74C3C', width=2, dash='dash'),
            hovertemplate='<b>Reality</b><br>Date: %{x}<br>Balance: $%{y:,.0f}<extra></extra>'
        ))
        
        # Highlight cash crunch zones (where reality line goes negative)
        cash_crunch_mask = balance_real < 0
        if cash_crunch_mask.any():
            crunch_dates = dates_real[cash_crunch_mask]
            crunch_values = balance_real[cash_crunch_mask]
            
            fig.add_trace(go.Scatter(
                x=crunch_dates,
                y=crunch_values,
                mode='markers',
                name='🔴 Cash Crunch',
                marker=dict(color='red', size=10, symbol='x'),
                hovertemplate='<b>CASH CRUNCH!</b><br>Date: %{x}<br>Balance: $%{y:,.0f}<extra></extra>'
            ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dot", line_color="gray", annotation_text="Break-even")
    
    fig.update_layout(
        title='<b>Cumulative Cash Flow: Optimistic vs Reality</b>',
        xaxis_title='Date',
        yaxis_title='Cumulative Cash Balance ($)',
        template='plotly_white',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cash crunch warning
    if show_reality and (balance_real < 0).any():
        min_balance = balance_real.min()
        min_date = dates_real[balance_real.idxmin()]
        st.error(f"⚠️ **Cash Crunch Warning**: Your balance will drop to **${min_balance:,.0f}** on **{min_date.strftime('%Y-%m-%d')}** if delays persist!")


def plot_cash_flow(transactions):
    """
    Legacy function for backward compatibility - plots simple cumulative cash flow.
    
    Args:
        transactions (DataFrame): Transaction data.
    """
    transactions = transactions.copy()
    transactions['Date'] = pd.to_datetime(transactions['Date'])
    transactions.sort_values('Date', inplace=True)

    cumulative_cash_flow = transactions.groupby('Date')['Amount'].sum().cumsum()
    cash_crunch = cumulative_cash_flow[cumulative_cash_flow < 0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cumulative_cash_flow.index,
        y=cumulative_cash_flow,
        mode='lines',
        name='Cumulative Cash Flow'
    ))
    
    if not cash_crunch.empty:
        fig.add_trace(go.Scatter(
            x=cash_crunch.index,
            y=cash_crunch,
            mode='markers',
            name='Cash Crunch',
            marker=dict(color='red', size=10)
        ))

    fig.update_layout(
        title='Cumulative Cash Flow Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Cash Flow',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def highlight_cash_crunch(cumulative_cash_flow):
    """
    Identify cash crunch periods (negative balance).
    
    Args:
        cumulative_cash_flow (Series): Cumulative cash flow data.
        
    Returns:
        Series: Periods with negative balance.
    """
    return cumulative_cash_flow[cumulative_cash_flow < 0]