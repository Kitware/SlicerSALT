/*==============================================================================

  Program: 3D Slicer

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAppAboutDialog_h
#define __qAppAboutDialog_h

// Qt includes
#include <QDialog>

// CTK includes
#include <ctkPimpl.h>

// SlicerSALT includes
#include "qSlicerSALTAppExport.h"

class qAppAboutDialogPrivate;

/// Pre-request that a qSlicerApplication has been instanced
class Q_SLICERSALT_APP_EXPORT qAppAboutDialog :
  public QDialog
{
  Q_OBJECT
public:
  qAppAboutDialog(QWidget *parentWidget = nullptr);
  ~qAppAboutDialog() override;

  Q_INVOKABLE void setLogo(const QPixmap& newLogo);

protected:
  QScopedPointer<qAppAboutDialogPrivate> d_ptr;
  QString acknowledgment() const;
  QString copyrights() const;

private:
  Q_DECLARE_PRIVATE(qAppAboutDialog);
  Q_DISABLE_COPY(qAppAboutDialog);
};

#endif
