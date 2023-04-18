import faker from 'faker';

function getRandomInt(max) {
    return Math.floor(20 + Math.random() * max);
}

function generateObjectId() {
    var timestamp = ((new Date().getTime() / 1000) | 0).toString(16);
    return (
        timestamp +
        "xxxxxxxxxxxxxxxx"
            .replace(/[x]/g, function () {
                return ((Math.random() * 16) | 0).toString(16);
            })
            .toLowerCase()
    );
}

const ticketsNumber = getRandomInt(10);
const racesNumber = getRandomInt(10);
const passenger_ids = [];
const ticket_ids = [];
const race_ids = [];

for (let i = 0; i < ticketsNumber; i++) {
    passenger_ids[i] = generateObjectId();
    ticket_ids[i] = generateObjectId();
    race_ids[i] = generateObjectId();
}

for (let i = 0; i < racesNumber; i++) {
    race_ids[i] = generateObjectId();
}

function getTicketTemplate(index, passenger_id, ticket_id) {
    const gender = faker.name.gender(true);
    const firstName = faker.name.firstName(gender);
    const secondName = faker.name.lastName(gender);
    const email = faker.internet.email(firstName, secondName);
    const phone = faker.phone.phoneNumber("+48 ## ### ## ##");
    const job = faker.name.jobType();
    const age = faker.random.number({ max: 100 })
    const country = faker.address.county();
    const city = faker.address.city();
    const street = faker.address.streetAddress(true);
    const buyDate = faker.date.between(new Date(2010, 0, 1), new Date());

    return {
        index: index,
        doc_type: "ticket",
        id: ticket_id,
        body: {
            id: passenger_id,
            personal_data: `${gender} ${firstName} ${secondName} ${email} ${phone} ${job} ${age} ${country} ${city} ${street}`,
            buy_date: buyDate.toISOString(),
            amount: faker.finance.amount(1000, 10000),
            race_id: race_ids[faker.random.number({ max: racesNumber })]
        }
    };
}
function getRaceInfo() {
    const planes = ['Airbus', 'Boeing', 'Cessna', 'Craic', 'Comna', 'Иркут'];
    const companies = ['Utair', 'Catar', 'Ural', 'Aeroflot', 'Turkish', 'Fly one', 'Azur', 'Malta'];
    return planes[faker.random.number({ max: planes.length - 1 })] + ' ' + companies[faker.random.number({ max: companies.length - 1 })];
}

const tickets = [];
const races = [];

for (let i = 0; i < ticketsNumber; i++) {
    tickets[i] = getTicketTemplate(i, passenger_ids[i], ticket_ids[i]);
}

function addRandomHours(date: Date) {
    const newDate = new Date(date).setHours(new Date(date).getHours() + faker.random.number({ max: 24 }));
    return new Date(newDate).toISOString();
}

function getRaceTemplate(index, race_id) {
    const ticket = tickets.find((ticket) => ticket.body.race_id === race_id);
    const date_out = faker.date.between(new Date(ticket && ticket.buy_date ? ticket.buy_date : '2009-12-31T21:00:00.000Z'), new Date());
    const date_out_fact = addRandomHours(date_out);

    return {
        index: index,
        doc_type: "race",
        id: race_id,
        body: {
            "race_number": faker.random.number({ min: 100, max: 1000 }),
            "info": getRaceInfo(),
            "from": `${faker.address.county()} ${faker.address.city()}`,
            "to": `${faker.address.county()} ${faker.address.city()}`,
            "sold_tickets_count": faker.random.number({ max: 100 }),
            "remaining_tickets_count": faker.random.number({ max: 100 }),
            "date_out": date_out.toISOString(),
            "date_out_fact": date_out_fact,
            "date_in": addRandomHours(date_out_fact),
            "date_in_fact": addRandomHours(date_out_fact)
        }
    };
}



for (let i = 0; i < racesNumber; i++) {
    races[i] = getRaceTemplate(i, race_ids[i]);
}

console.log(JSON.stringify(tickets));
console.log(JSON.stringify(races));
