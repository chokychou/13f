import pg from 'pg'
const { Client } = pg


export default async function MatchIssuers(text_to_match, target = 'localhost:50051') {
    if (!text_to_match) {
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
 
    const result = await client.query('SELECT * FROM SEC_FILINGS.CUSIP_METADATA WHERE cusip ILIKE $1 OR name ILIKE $1', [`%${text_to_match}%`]);

    await client.end();

    return result.rows;
}
