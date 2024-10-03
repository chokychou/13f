import pg from 'pg'
const { Client } = pg


// TODO: Implement
function ReadRowsFromCacheServer(cusip) {
    return [];
}
// TODO: Implement
function CacheRowsInCacheServer(cusip, rows) {
    return rows
}

// Return rows from CacheServer if there is a cusip entry. Else, run the online query and cache in CacheServer.
export default async function RequestIssuerStats(cusip, graph = 1, target = 'localhost:50051') {
    if (!cusip) {
        throw new Error('Cusip is required');
    }

    const client = new Client({
        host: "127.0.0.1",  
        database: "postgres",  
        user: "test_user", 
        password: "test_pw",  
        port: "5432"
    });

    await client.connect();

    const cached_rows = ReadRowsFromCacheServer(cusip);
    if (cached_rows.length > 0) {
        return cached_rows;
    }

    const result = await client.query('SELECT * FROM SEC_FILINGS.CUSIP_OWNERSHIP AS t1 INNER JOIN SEC_FILINGS.CIK_METADATA AS t2 ON t1.cik = t2.cik WHERE t1.cusip = $1', [cusip]);

    await client.end();

    return CacheRowsInCacheServer(cusip, result.rows);
}

