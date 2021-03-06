import React from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

const Theme = ({ children }) => {
  const theme = useSelector((state) => (state.profile.preferences.theme));
  const materialTheme = createMuiTheme({
    palette: {
      type: theme || 'light'
    }
  });

  return (
    <ThemeProvider theme={materialTheme}>
      <CssBaseline />
      { children }
    </ThemeProvider>
  );
};

Theme.propTypes = {
  children: PropTypes.node.isRequired
};

export default Theme;
