import '../styles/FilterItem.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';

function FilterItem({ filter }) {
  return (
    <div key={filter.friendly_name} className="createPost__form__radio">
      <Form.Check type="checkbox" id={filter.id} name="selected_filter" value={filter.id} label={filter.friendly_name} />
      <OverlayTrigger
        key={filter.id}
        trigger="click"
        placement="top"
        overlay={
        (
          <Card
            key={filter.id}
            style={{ width: '18rem', 'z-index': '1000000' }}
          >
            <Card.Img variant="top" src={filter.example_url} />
            <Card.Body>
              <Card.Title>{filter.friendly_name}</Card.Title>
              <Card.Text>
                {filter.description}
              </Card.Text>
            </Card.Body>
          </Card>
        )
     }>
        <Button>Show Detailsyyyy</Button>
      </OverlayTrigger>
    </div>
  );
}

export default FilterItem;
