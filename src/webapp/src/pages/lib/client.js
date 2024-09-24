import pg from 'pg'
const { Client } = pg

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
 
    const result = await client.query('SELECT * FROM SEC_FILINGS.CUSIP_OWNERSHIP WHERE cusip = $1', [cusip]);

    await client.end();

    return result.rows;
}
 
