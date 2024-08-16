// Get 13F.
// Usage: http://localhost:3000/api/match_issuer?text=002824100

import MatchIssuers from '../lib/issuer_match_client'

export default async function handler(req, res) {
  var text = req.query.text
  if (!text) {
    res.status(400).send({ error: 'text is required to match' })
    return
  }
  try {
    const result = await MatchIssuers(text)
    res.status(200).send({ result })
  } catch (err) {
    res.status(500).send({ error: 'failed to fetch data' })
  }
}