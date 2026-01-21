const ticketList = document.querySelector('#ticket-list');
const details = document.querySelector('#details');
const form = document.querySelector('#ticket-form');
const titleInput = document.querySelector('#title');
const descriptionInput = document.querySelector('#description');
const priorityInput = document.querySelector('#priority');

const tickets = [
  { id: 124, title: 'Printer virker ikke', description: 'Skriver ikke ut fra maskin i 3. etasje.', priority: 'Middels', status: 'Åpen' },
  { id: 123, title: 'Mangler tilgang', description: 'Får ikke åpnet CRM-appen.', priority: 'Høy', status: 'Åpen' }
];

let nextId = 125;
let selectedId = tickets[0]?.id ?? null;

const renderDetails = (ticket) => {
  if (!ticket) {
    details.innerHTML = '<p>Velg en ticket fra listen for å se detaljer her.</p>';
    return;
  }

  details.innerHTML = `
    <p><strong>#${ticket.id} ${ticket.title}</strong></p>
    <p>Status: ${ticket.status}</p>
    <p>Prioritet: ${ticket.priority}</p>
    <p>${ticket.description}</p>
  `;
};

const renderList = () => {
  ticketList.innerHTML = '';

  tickets.forEach((ticket) => {
    const li = document.createElement('li');
    li.className = 'ticket' + (ticket.id === selectedId ? ' active' : '');
    li.innerHTML = `
      <h4>#${ticket.id} ${ticket.title}</h4>
      <small>Prioritet: ${ticket.priority} · Status: ${ticket.status}</small>
    `;

    li.addEventListener('click', () => {
      selectedId = ticket.id;
      renderList();
      renderDetails(ticket);
    });

    ticketList.appendChild(li);
  });
};

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();
  const description = descriptionInput.value.trim();
  const priority = priorityInput.value;
  if (!title || !description) return;

  const newTicket = {
    id: nextId++,
    title,
    description,
    priority,
    status: 'Åpen'
  };

  tickets.unshift(newTicket);
  selectedId = newTicket.id;
  renderList();
  renderDetails(newTicket);
  form.reset();
});

renderList();
renderDetails(tickets.find((ticket) => ticket.id === selectedId));