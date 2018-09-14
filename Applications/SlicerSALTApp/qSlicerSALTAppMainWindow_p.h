/* Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
   file LICENSE.  */

#ifndef __qSlicerSALTAppMainWindow_p_h
#define __qSlicerSALTAppMainWindow_p_h

// SlicerSALT includes
#include "qSlicerSALTAppMainWindow.h"

// Slicer includes
#include "qSlicerMainWindow_p.h"

//-----------------------------------------------------------------------------
class Q_SLICERSALT_APP_EXPORT qSlicerSALTAppMainWindowPrivate
  : public qSlicerMainWindowPrivate
{
  Q_DECLARE_PUBLIC(qSlicerSALTAppMainWindow);
public:
  typedef qSlicerMainWindowPrivate Superclass;
  qSlicerSALTAppMainWindowPrivate(qSlicerSALTAppMainWindow& object);
  virtual ~qSlicerSALTAppMainWindowPrivate();

  virtual void init();
  /// Reimplemented for custom behavior
  virtual void setupUi(QMainWindow * mainWindow);
};

#endif
