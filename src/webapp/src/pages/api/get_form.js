// Get 13F.
// Usage: http://localhost:3000/api/get_form?cusip=002824100

import RequestIssuerStats from '../lib/client'

export default async function handler(req, res) {
  var cusip = req.query.cusip
  if (!cusip) {
    res.status(400).send({ error: 'cusip is required' })
    return
  }
  try {
    const result = await RequestIssuerStats(cusip)
    res.status(200).send({ result })
  } catch (err) {
    res.status(500).send({ error: 'failed to fetch data' })
  }
}