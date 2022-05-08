import '../styles/FilterItem.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Form from 'react-bootstrap/Form';
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';

function FilterItem({ filter }) {
  const [checked, setChecked] = useState(false);
  return (
    <div key={filter.friendly_name} className="filter__item">
      <Stack direction="horizontal" gap={3} onClick={() => { setChecked(!checked); }}>
        <Form.Check type="checkbox" id={filter.id} name="selected_filter" value={filter.id} checked={checked} readOnly />
        <Stack gap={5}>
          <h1 className="filter__item__title mx-auto">{filter.friendly_name}</h1>
          <p className="mx-auto">{filter.description}</p>
        </Stack>
        <Image
          className="filter__item__image"
          src={filter.example_url}
          fluid
        />
      </Stack>
    </div>
  );
}

export default FilterItem;
