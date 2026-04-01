import React, { useState, useEffect } from 'react';

function App() {
  const [accounts, setAccounts] = useState([]);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Placeholder for customer ID - in a real app, this would come from authentication
  const customerId = 1;

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const response = await fetch(`/api/v1/customer/${customerId}/accounts`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAccounts(data);
        if (data.length > 0) {
          setSelectedAccount(data[0]);
        }
      } catch (e) {
        setError("Failed to fetch accounts.");
        console.error("Error fetching accounts:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchAccounts();
  }, [customerId]);

  useEffect(() => {
    const fetchTransactions = async () => {
      if (selectedAccount) {
        try {
          setLoading(true);
          const response = await fetch(`/api/v1/customer/${customerId}/accounts/${selectedAccount.id}/transactions`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setTransactions(data);
        } catch (e) {
          setError("Failed to fetch transactions.");
          console.error("Error fetching transactions:", e);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchTransactions();
  }, [selectedAccount, customerId]);

  if (loading) return <div className='flex justify-center items-center h-screen'>Loading...</div>;
  if (error) return <div className='flex justify-center items-center h-screen text-red-500'>Error: {error}</div>;

  return (
    <div className='min-h-screen bg-gray-100 p-4'>
      <header className='bg-white shadow-sm p-4 rounded-lg mb-4'>
        <h1 className='text-2xl font-semibold text-gray-800'>Account Overview</h1>
      </header>

      <div className='grid grid-cols-1 md:grid-cols-3 gap-4 mb-4'>
        {accounts.map((account) => (
          <div
            key={account.id}
            className={`bg-white p-6 rounded-lg shadow-md cursor-pointer ${selectedAccount?.id === account.id ? 'border-2 border-blue-500' : ''}`}
            onClick={() => setSelectedAccount(account)}
          >
            <h2 className='text-xl font-medium text-gray-700'>{account.account_type}</h2>
            <p className='text-gray-500'>Account Number: {account.account_number}</p>
            <p className='text-2xl font-bold text-gray-900'>Balance: ${account.balance.toFixed(2)}</p>
          </div>
        ))}
      </div>

      {selectedAccount && (
        <section className='bg-white p-6 rounded-lg shadow-md'>
          <h2 className='text-xl font-semibold text-gray-800 mb-4'>Transactions for {selectedAccount.account_type}</h2>
          {
            transactions.length > 0 ? (
              <div className='overflow-x-auto'>
                <table className='min-w-full divide-y divide-gray-200'>
                  <thead className='bg-gray-50'>
                    <tr>
                      <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>Date</th>
                      <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>Description</th>
                      <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>Type</th>
                      <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>Amount</th>
                    </tr>
                  </thead>
                  <tbody className='bg-white divide-y divide-gray-200'>
                    {transactions.map((transaction) => (
                      <tr key={transaction.id}>
                        <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-500'>{new Date(transaction.timestamp).toLocaleDateString()}</td>
                        <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>{transaction.description}</td>
                        <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-500'>{transaction.type}</td>
                        <td className={`px-6 py-4 whitespace-nowrap text-sm ${transaction.type === 'deposit' ? 'text-green-600' : 'text-red-600'}`}>
                          {transaction.type === 'deposit' ? '+' : '-'}${transaction.amount.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className='text-gray-500'>No transactions found for this account.</p>
            )
          }
        </section>
      )}
    </div>
  );
}

export default App;
