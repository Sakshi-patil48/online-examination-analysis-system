import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

export default function Breadcrumbs({ items }) {
  if (!items || items.length === 0) return null;

  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <React.Fragment key={index}>
            {index > 0 && <ChevronRight size={14} color="#94a3b8" />}
            {isLast ? (
              <span className="current">{item.label}</span>
            ) : (
              <Link to={item.path || '#'}>{item.label}</Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
}
