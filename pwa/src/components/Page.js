import React from 'react';

import { Breadcrumb, BreadcrumbItem } from 'reactstrap';

const Page = ({
  title,
  breadcrumbs,
  tag: Tag,
  className,
  children,
  ...restProps
}) => {
  const classes = 'cr-page px-3 '+className;

  return (
    <Tag className={classes} {...restProps}>
      <div className="cr-page__header">
        {title && typeof title === 'string' ? (
          <h1 className="cr-page__title">
            {title}
          </h1>
        ) : (
            title
          )}
        {breadcrumbs && (
          <Breadcrumb className="cr-page__breadcrumb">
            <BreadcrumbItem>Home</BreadcrumbItem>
            {breadcrumbs.length &&
              breadcrumbs.map(({ name, active }, index) => (
                <BreadcrumbItem key={index} active={active}>
                  {name}
                </BreadcrumbItem>
              ))}
          </Breadcrumb>
        )}
      </div>
      {children}
    </Tag>
  );
};


Page.defaultProps = {
  tag: 'div',
  title: '',
};

export default Page;
