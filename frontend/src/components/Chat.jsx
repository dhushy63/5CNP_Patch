
import React, { useState } from 'react'
import { apiPost } from '../lib/api'

export default function Chat({ userId }) {
  const [input, setInput] = useState('low-GI breakfast ideas?')
  const [reply, setReply] = useState('')

  const send = async () => { setReply('...sending...')
    try {
      const res = await apiPost('/interrupt', { user_id: userId, query: input })
      setReply(res.reply || JSON.stringify(res))
    } catch (e) { console.error(e);
      setReply(String(e))
    }
  }

  return (
    <div style={{ maxWidth: 720 }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <input value={input} onChange={e=>setInput(e.target.value)} style={{ flex: 1, padding: 10, borderRadius: 12, border: '1px solid #ddd' }}/>
        <button onClick={send} style={{ padding: '8px 16px', borderRadius: 12, border: '1px solid #ddd' }}>Send</button>
      </div>
      <div style={{ marginTop: 16, padding: 12, border: '1px solid #eee', borderRadius: 12, background: '#fafafa' }}>
        {reply || 'Ask something to the (stubbed) agent...'}
      </div>
    </div>
  )
}
