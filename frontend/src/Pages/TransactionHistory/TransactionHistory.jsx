const TransactionHistory = () => {
    return (
        <div className="transaction-history-container">
            <h2>Transaction History</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Map through transaction history data and display rows */}
                </tbody>
            </table>
        </div>
    );
} 
export default TransactionHistory;