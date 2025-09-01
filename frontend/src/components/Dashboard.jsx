
import React, { useEffect, useState } from 'react'
import { apiGet } from '../lib/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar } from 'recharts'

export default function Dashboard({ userId }) {
  const [greet, setGreet] = useState({ name: 'User', city: 'City', diet: '', message: 'Hello!', latest_cgm: null, conditions: [] })
  const [err, setErr] = useState('')
  const [cgm, setCgm] = useState([])
  const [mood, setMood] = useState([])

  useEffect(()=>{
    apiGet(`/greet?user_id=${userId}`).then(setGreet).catch(e=>setErr(String(e)))
    apiGet(`/cgm/recent?user_id=${userId}`).then(d=>setCgm(d.series || [])).catch(e=>setErr(String(e)))
    apiGet(`/mood/recent?user_id=${userId}`).then(d=>setMood(d.series || [])).catch(e=>setErr(String(e)))
  }, [userId])

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3>{greet.message}</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {greet.latest_cgm != null && (
            <span style={pill('#e8f7ef')}>Latest CGM: {Math.round(greet.latest_cgm)} mg/dL</span>
          )}
          {Array.isArray(greet.conditions) && greet.conditions.length > 0 && (
            <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
              {greet.conditions.map((c,i)=>(<span key={i} style={pill('#eef3ff')}>{c}</span>))}
            </div>
          )}
        </div>
      </div>
      <p style={{ color: '#6b7280' }}>(last 7 days)</p>

      {greet.diet && (
        <div style={{ display:'flex', gap:8, margin:'6px 0 14px 0' }}>
          <span style={pill('#fff7ed')}>Diet: {greet.diet}</span>
        </div>
      )}

      {err && (<div style={{color:'#b91c1c', marginBottom:12}}>Error: {err}</div>)}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div style={card()}>
          <h4>CGM</h4>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <LineChart data={cgm}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="ts" hide />
                <YAxis domain={[70, 220]} />
                <Tooltip />
                <Line type="monotone" dataKey="value" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <small>Points: {cgm.length}</small>
        </div>

        <div style={card()}>
          <h4>Mood Scores</h4>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={mood}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <small>Points: {mood.length}</small>
        </div>
      </div>
    </div>
  )
}

function pill(bg) {
  return { background: bg, borderRadius: 999, padding: '6px 10px', border: '1px solid #e5e7eb' }
}
function card() {
  return { background: '#fff', border: '1px solid #e5e7eb', borderRadius: 16, padding: 16 }
}
