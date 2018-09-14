/* Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
   file LICENSE.  */

#ifndef __qSlicerSALTAppMainWindow_h
#define __qSlicerSALTAppMainWindow_h

// SlicerSALT includes
#include "qSlicerSALTAppExport.h"
class qSlicerSALTAppMainWindowPrivate;

// Slicer includes
#include "qSlicerMainWindow.h"

class Q_SLICERSALT_APP_EXPORT qSlicerSALTAppMainWindow : public qSlicerMainWindow
{
  Q_OBJECT
public:
  typedef qSlicerMainWindow Superclass;

  qSlicerSALTAppMainWindow(QWidget *parent=0);
  virtual ~qSlicerSALTAppMainWindow();

public:
  virtual void show();

public slots:
  void on_HelpAboutSlicerSALTAppAction_triggered();

protected:
  qSlicerSALTAppMainWindow(qSlicerSALTAppMainWindowPrivate* pimpl, QWidget* parent);

private:
  Q_DECLARE_PRIVATE(qSlicerSALTAppMainWindow);
  Q_DISABLE_COPY(qSlicerSALTAppMainWindow);
};

#endif
