
import React, { useState } from 'react'
import Dashboard from './components/Dashboard.jsx'
import Chat from './components/Chat.jsx'
import LogFood from './components/LogFood.jsx'
import MealPlan from './components/MealPlan.jsx'

export default function App() {
  const [tab, setTab] = useState('dashboard')
  const [userId, setUserId] = useState(1)

  return (
    <div style={{ fontFamily: 'Inter, system-ui, Arial', padding: 24 }}>
      <h1 style={{ fontSize: 32, fontWeight: 800 }}>5CNP</h1>

      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
        <label>User ID:</label>
        <input value={userId} onChange={e=>setUserId(parseInt(e.target.value||'1',10))}
               style={{ width: 80, padding: 6, borderRadius: 8, border: '1px solid #ccc' }}/>

        <div style={{ display: 'flex', gap: 8, marginLeft: 12 }}>
          <button onClick={()=>setTab('dashboard')} style={btn(tab==='dashboard')}>Dashboard</button>
          <button onClick={()=>setTab('chat')} style={btn(tab==='chat')}>Chat</button>
          <button onClick={()=>setTab('logfood')} style={btn(tab==='logfood')}>Log Food</button>
          <button onClick={()=>setTab('mealplan')} style={btn(tab==='mealplan')}>Meal Plan</button>
        </div>
      </div>

      {tab === 'dashboard' && <Dashboard userId={userId} />}
      {tab === 'chat' && <Chat userId={userId} />}
      {tab === 'logfood' && <LogFood userId={userId} />}
      {tab === 'mealplan' && <MealPlan userId={userId} />}
    </div>
  )
}

function btn(active) {
  return {
    padding: '8px 14px',
    borderRadius: 20,
    border: '1px solid #ddd',
    background: active ? '#6c4df6' : '#fff',
    color: active ? '#fff' : '#111',
    cursor: 'pointer'
  }
}
